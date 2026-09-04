"""
MSG91 OTP Integration Tests
Verifies provider selection, credential validation, error surfacing (including
MSG91's HTTP-200-with-error-body case), rollback on failure, and no code leaks.
"""
import pytest
from app.config import settings, validate_production_settings
from app.services.citizen_auth_service import (
    CitizenAuthService, Msg91OtpProvider, get_otp_provider,
    normalize_indian_phone, hash_phone
)
from app.models import OtpChallenge


def _set_msg91(monkeypatch, auth_key="key_test123", template_id="tpl_test123", sender_id=None):
    monkeypatch.setattr(settings, "OTP_MODE", "MSG91")
    monkeypatch.setattr(settings, "MSG91_AUTH_KEY", auth_key)
    monkeypatch.setattr(settings, "OTP_SMS_PROVIDER_API_KEY", None)
    monkeypatch.setattr(settings, "MSG91_TEMPLATE_ID", template_id)
    monkeypatch.setattr(settings, "MSG91_SENDER_ID", sender_id)
    monkeypatch.setattr(settings, "OTP_SMS_SENDER_ID", None)


def test_msg91_provider_selected_when_mode_msg91(monkeypatch):
    _set_msg91(monkeypatch)
    assert isinstance(get_otp_provider(), Msg91OtpProvider)


def test_msg91_missing_auth_key_raises(monkeypatch):
    _set_msg91(monkeypatch, auth_key=None)
    with pytest.raises(RuntimeError, match="MSG91 auth key not configured"):
        Msg91OtpProvider().send_otp("+91982009901", "123456")


def test_msg91_missing_template_raises(monkeypatch):
    _set_msg91(monkeypatch, template_id=None)
    with pytest.raises(RuntimeError, match="MSG91 template not configured"):
        Msg91OtpProvider().send_otp("+91982009901", "123456")


def test_config_validation_requires_template(monkeypatch):
    _set_msg91(monkeypatch, template_id=None)
    with pytest.raises(RuntimeError, match="MSG91_TEMPLATE_ID"):
        validate_production_settings()


def test_config_validation_requires_auth_key(monkeypatch):
    _set_msg91(monkeypatch, auth_key=None)
    with pytest.raises(RuntimeError, match="MSG91_AUTH_KEY"):
        validate_production_settings()


class FakeResponse:
    def __init__(self, status_code, body=None):
        self.status_code = status_code
        self._body = body if body is not None else {}

    def json(self):
        return self._body


def _patch_requests_post(monkeypatch, fake_response):
    import requests as real_requests
    calls = []

    def fake_post(url, json=None, params=None, headers=None, timeout=None):
        calls.append({"url": url, "json": json, "params": params, "headers": headers})
        return fake_response

    monkeypatch.setattr(real_requests, "post", fake_post)
    return calls


def test_msg91_otp_api_success(db_session, monkeypatch):
    """v5 OTP API success path (no custom sender)."""
    _set_msg91(monkeypatch)
    calls = _patch_requests_post(monkeypatch, FakeResponse(200, {"type": "success"}))
    res = Msg91OtpProvider().send_otp("+91982009901", "483920")
    assert res["provider"] == "MSG91"
    assert res["status"] == "SENT"
    assert res["delivered"] is True
    # Correct endpoint and phone format (91 prefix, no '+')
    assert calls[0]["url"] == "https://control.msg91.com/api/v5/otp"
    assert calls[0]["params"]["mobile"] == "91982009901"
    assert calls[0]["params"]["otp"] == "483920"
    assert calls[0]["params"]["template_id"] == "tpl_test123"
    # Auth key goes in header, never in URL
    assert calls[0]["headers"]["authkey"] == "key_test123"
    assert "key_test123" not in calls[0]["url"]


def test_msg91_flow_api_used_with_custom_sender(monkeypatch):
    """Custom DLT sender switches to the Flow API with correct payload."""
    _set_msg91(monkeypatch, sender_id="AAROGY")
    calls = _patch_requests_post(monkeypatch, FakeResponse(200, {"type": "success"}))
    res = Msg91OtpProvider().send_otp("+91982009901", "483920")
    assert res["status"] == "SENT"
    assert calls[0]["url"] == "https://control.msg91.com/api/v5/flow/"
    assert calls[0]["json"]["sender"] == "AAROGY"
    assert calls[0]["json"]["recipients"] == [{"mobiles": "91982009901", "OTP": "483920"}]


def test_msg91_http_error_surfaces_actionable_message(monkeypatch):
    _set_msg91(monkeypatch)
    _patch_requests_post(monkeypatch, FakeResponse(401, {"type": "error", "message": "Invalid auth key"}))
    with pytest.raises(RuntimeError, match="MSG91 rejected SMS delivery.*Invalid auth key"):
        Msg91OtpProvider().send_otp("+91982009901", "123456")


def test_msg91_http_200_with_error_body_raises(monkeypatch):
    """MSG91 sometimes returns HTTP 200 with type=error (e.g. balance exhausted) - must raise."""
    _set_msg91(monkeypatch)
    _patch_requests_post(monkeypatch, FakeResponse(200, {"type": "error", "message": "Insufficient balance"}))
    with pytest.raises(RuntimeError, match="Insufficient balance"):
        Msg91OtpProvider().send_otp("+91982009901", "123456")


def test_failed_dispatch_rolls_back_challenge_for_immediate_retry(db_session, monkeypatch):
    _set_msg91(monkeypatch)
    monkeypatch.setattr(settings, "ENVIRONMENT", "staging")

    class ExplodingProvider:
        def send_otp(self, phone_norm, otp_code):
            raise RuntimeError("MSG91 rejected SMS delivery (HTTP 200). Insufficient balance")

    monkeypatch.setattr(
        "app.services.citizen_auth_service.get_otp_provider",
        lambda: ExplodingProvider()
    )

    phone = "9820099921"
    with pytest.raises(RuntimeError, match="Insufficient balance"):
        CitizenAuthService.request_otp(db_session, phone)

    # No challenge persisted -> user can retry immediately
    p_hash = hash_phone(normalize_indian_phone(phone))
    assert db_session.query(OtpChallenge).filter(OtpChallenge.phone_hash == p_hash).first() is None

    # Provider works now -> request succeeds
    class WorkingProvider:
        def send_otp(self, phone_norm, otp_code):
            return {"provider": "MSG91", "status": "SENT"}

    monkeypatch.setattr(
        "app.services.citizen_auth_service.get_otp_provider",
        lambda: WorkingProvider()
    )
    res = CitizenAuthService.request_otp(db_session, phone)
    assert res["provider"] == "MSG91"


def test_successful_dispatch_commits_challenge_and_no_code_leak(db_session, monkeypatch):
    _set_msg91(monkeypatch)
    monkeypatch.setattr(settings, "ENVIRONMENT", "staging")

    class WorkingProvider:
        def send_otp(self, phone_norm, otp_code):
            return {"provider": "MSG91", "status": "SENT"}

    monkeypatch.setattr(
        "app.services.citizen_auth_service.get_otp_provider",
        lambda: WorkingProvider()
    )

    phone = "9820099922"
    res = CitizenAuthService.request_otp(db_session, phone)
    assert res["provider"] == "MSG91"
    assert "mock_code" not in res  # live provider never leaks the OTP

    p_hash = hash_phone(normalize_indian_phone(phone))
    challenge = db_session.query(OtpChallenge).filter(
        OtpChallenge.phone_hash == p_hash,
        OtpChallenge.consumed_at.is_(None)
    ).first()
    assert challenge is not None
