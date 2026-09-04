"""
Twilio OTP Integration Tests
Verifies provider selection, credential validation, error surfacing,
and rollback behavior when Twilio rejects a dispatch.
"""
import pytest
from app.config import settings, validate_production_settings
from app.services.citizen_auth_service import (
    CitizenAuthService, TwilioOtpProvider, get_otp_provider,
    normalize_indian_phone, hash_phone
)
from app.models import OtpChallenge


def _set_twilio(monkeypatch, sid="AC_test123", token="token_test123", from_number="+1234567890", mss=None):
    monkeypatch.setattr(settings, "OTP_MODE", "TWILIO")
    monkeypatch.setattr(settings, "TWILIO_ACCOUNT_SID", sid)
    monkeypatch.setattr(settings, "TWILIO_AUTH_TOKEN", token)
    monkeypatch.setattr(settings, "TWILIO_FROM_NUMBER", from_number)
    monkeypatch.setattr(settings, "TWILIO_MESSAGING_SERVICE_SID", mss)


def test_twilio_provider_selected_when_mode_twilio(monkeypatch):
    _set_twilio(monkeypatch)
    assert isinstance(get_otp_provider(), TwilioOtpProvider)


def test_twilio_missing_all_credentials_raises(monkeypatch):
    _set_twilio(monkeypatch, sid=None, token=None, from_number=None, mss=None)
    with pytest.raises(RuntimeError, match="Twilio credentials not configured"):
        TwilioOtpProvider().send_otp("+91982009901", "123456")


def test_twilio_missing_sender_raises(monkeypatch):
    _set_twilio(monkeypatch, from_number=None, mss=None)
    with pytest.raises(RuntimeError, match="Twilio sender not configured"):
        TwilioOtpProvider().send_otp("+91982009901", "123456")


def test_twilio_messaging_service_sid_accepted_without_from_number(monkeypatch):
    """Messaging Service SID alone is a valid sender."""
    _set_twilio(monkeypatch, from_number=None, mss="MGtest123")
    provider = TwilioOtpProvider()
    assert provider.messaging_service_sid == "MGtest123"


def test_config_validation_requires_twilio_sender(monkeypatch):
    _set_twilio(monkeypatch, from_number=None, mss=None)
    with pytest.raises(RuntimeError, match="TWILIO_FROM_NUMBER or TWILIO_MESSAGING_SERVICE_SID"):
        validate_production_settings()


def test_config_validation_passes_with_messaging_service(monkeypatch):
    _set_twilio(monkeypatch, from_number=None, mss="MGtest123")
    validate_production_settings()  # should not raise


class FakeResponse:
    def __init__(self, status_code, body=None):
        self.status_code = status_code
        self._body = body or {}

    def json(self):
        return self._body


def test_twilio_rejection_surfaces_actionable_error(db_session, monkeypatch):
    """Twilio HTTP error must raise (not silently report SENT), with safe detail."""
    _set_twilio(monkeypatch)
    monkeypatch.setattr(settings, "ENVIRONMENT", "staging")

    class FakeRequests:
        @staticmethod
        def post(url, data=None, auth=None, timeout=None):
            return FakeResponse(21212, {"message": "Invalid To number", "code": 21212})

    # Patch requests.post directly (it is imported inside send_otp, same module object)
    import requests as real_requests
    monkeypatch.setattr(real_requests, "post", FakeRequests.post)

    with pytest.raises(RuntimeError, match="Twilio rejected SMS delivery.*Invalid To number"):
        TwilioOtpProvider().send_otp("+91982009901", "123456")


def test_failed_dispatch_rolls_back_challenge_for_immediate_retry(db_session, monkeypatch):
    """If provider fails, no challenge row is committed, so user can retry instantly."""
    _set_twilio(monkeypatch)
    monkeypatch.setattr(settings, "ENVIRONMENT", "staging")

    class ExplodingProvider:
        def send_otp(self, phone_norm, otp_code):
            raise RuntimeError("Twilio rejected SMS delivery (HTTP 400). test failure")

    monkeypatch.setattr(
        "app.services.citizen_auth_service.get_otp_provider",
        lambda: ExplodingProvider()
    )

    phone = "9820099911"
    with pytest.raises(RuntimeError, match="Twilio rejected"):
        CitizenAuthService.request_otp(db_session, phone)

    # No challenge persisted
    p_hash = hash_phone(normalize_indian_phone(phone))
    challenge = db_session.query(OtpChallenge).filter(
        OtpChallenge.phone_hash == p_hash
    ).first()
    assert challenge is None

    # Retry immediately succeeds (no cooldown error) once provider works
    class WorkingProvider:
        def send_otp(self, phone_norm, otp_code):
            return {"provider": "TWILIO", "status": "SENT"}

    monkeypatch.setattr(
        "app.services.citizen_auth_service.get_otp_provider",
        lambda: WorkingProvider()
    )
    res = CitizenAuthService.request_otp(db_session, phone)
    assert res["provider"] == "TWILIO"


def test_successful_dispatch_commits_challenge(db_session, monkeypatch):
    _set_twilio(monkeypatch)
    monkeypatch.setattr(settings, "ENVIRONMENT", "staging")

    class WorkingProvider:
        def send_otp(self, phone_norm, otp_code):
            return {"provider": "TWILIO", "status": "SENT"}

    monkeypatch.setattr(
        "app.services.citizen_auth_service.get_otp_provider",
        lambda: WorkingProvider()
    )

    phone = "9820099912"
    res = CitizenAuthService.request_otp(db_session, phone)
    assert res["provider"] == "TWILIO"
    assert "mock_code" not in res  # live provider never leaks the code

    p_hash = hash_phone(normalize_indian_phone(phone))
    challenge = db_session.query(OtpChallenge).filter(
        OtpChallenge.phone_hash == p_hash,
        OtpChallenge.consumed_at.is_(None)
    ).first()
    assert challenge is not None


def test_no_mock_code_leak_in_twilio_mode(db_session, monkeypatch):
    """Even in development env, TWILIO mode must never return mock_code."""
    _set_twilio(monkeypatch)
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")

    class WorkingProvider:
        def send_otp(self, phone_norm, otp_code):
            return {"provider": "TWILIO", "status": "SENT"}

    monkeypatch.setattr(
        "app.services.citizen_auth_service.get_otp_provider",
        lambda: WorkingProvider()
    )

    res = CitizenAuthService.request_otp(db_session, "9820099913")
    assert res["provider"] == "TWILIO"
    assert "mock_code" not in res
