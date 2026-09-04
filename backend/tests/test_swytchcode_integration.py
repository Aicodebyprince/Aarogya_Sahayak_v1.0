"""
Swytchcode Runtime Integration Tests.

Validates the Swytchcode execution layer end-to-end:
- Adapter bootstrap (Runtime SDK load, tooling.json detection)
- Kernel execution envelope (mock + governance fallback paths)
- Emergency dispatch idempotency engine
- Voice governance policies (language allowlist)
- Router endpoints (/api/swytchcode/*)
- Guardrail artifacts (policies.json, network allowlist)

These tests run fully offline (no network) - live kernel calls are only
attempted when SWYTCHCODE_MODE=live with connected credentials, and must
degrade gracefully when absent (Swytchcode Runtime invariant: zero demo crashes).
"""
import json
import os
import pytest

from app.config import settings


@pytest.fixture()
def adapter():
    from app.integrations.swytchcode import swytchcode_adapter
    return swytchcode_adapter


BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestSwytchcodeBootstrap:
    """Adapter must boot cleanly in every environment."""

    def test_adapter_boots_with_execution_path(self, adapter):
        status = adapter.get_status()
        assert status["execution_path"] in ("NATIVE_RUNTIME_SDK", "CLOUD_API", "GOVERNOR_FALLBACK", "NONE")
        assert status["runtime_sdk_loaded"] is True or status["execution_path"] != "NATIVE_RUNTIME_SDK"

    def test_project_initialized_with_tooling_json(self, adapter):
        assert adapter.project_initialized is True
        assert os.path.exists(os.path.join(BACKEND_ROOT, ".swytchcode", "tooling.json"))

    def test_registered_methods_detected(self, adapter):
        expected = {
            "sarvam_apis.translate.create",
            "sarvam_apis.transliterate.create",
            "sarvam_apis.stream.create",
            "gemini.model.modelgenerateContent.create",
        }
        assert expected.issubset(set(adapter.registered_methods))

    def test_installed_integrations_detected(self, adapter):
        integrations = set(adapter.installed_integrations)
        assert "Sarvam ai.sarvam_apis" in integrations
        assert "Gemini.gemini" in integrations


class TestGovernanceArtifacts:
    """Guardrail artifacts committed alongside the project."""

    def test_policies_json_valid(self):
        path = os.path.join(BACKEND_ROOT, ".swytchcode", "integrations", "policies.json")
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data.get("policies"), list) and len(data["policies"]) >= 3
        for pol in data["policies"]:
            assert pol["id"]
            assert pol["action"]["type"] in ("POLICY_BLOCKED", "AUTH_FAILED", "QUOTA_EXCEEDED", "RATE_LIMITED")

    def test_network_allowlist_restricts_hosts(self):
        path = os.path.join(BACKEND_ROOT, ".swytchcode", "tooling.json")
        with open(path, "r", encoding="utf-8") as f:
            tooling = json.load(f)
        allowed = tooling.get("permissions", {}).get("network", [])
        assert "api.sarvam.ai" in allowed
        assert "generativelanguage.googleapis.com" in allowed


class TestKernelExecutionEnvelope:
    """kernel_execute must always return a normalized envelope, never raise."""

    def test_kernel_execute_returns_envelope(self, adapter):
        env = adapter.kernel_execute(
            "sarvam_apis.translate.create",
            {"body": {"input": "test", "source_language_code": "en-IN", "target_language_code": "hi-IN"}},
        )
        assert env["status"] in ("SUCCESS", "ERROR", "EXCEPTION", "UNCONFIGURED")
        assert "trace" in env
        assert env["trace"]["canonical_id"] == "sarvam_apis.translate.create"
        assert env["trace"]["exec_path"] in ("NATIVE_RUNTIME_SDK", "CLOUD_API", "GOVERNOR_FALLBACK")

    def test_exec_translate_never_raises(self, adapter):
        result = adapter.exec_translate("hello", "en-IN", "hi-IN")
        assert result["status"] in ("SUCCESS", "ERROR", "EXCEPTION", "UNCONFIGURED")
        assert "translated_text" in result
        assert result["translated_text"] == "hello"  # passthrough on failure

    def test_exec_gemini_never_raises(self, adapter):
        result = adapter.exec_gemini_generate("test prompt")
        assert result["status"] in ("SUCCESS", "ERROR", "EXCEPTION", "UNCONFIGURED")
        assert result["provider"] == "SWYTCHCODE_KERNEL_GEMINI"

    def test_kernel_live_false_in_mock_mode(self, adapter):
        if adapter.mode.lower() == "mock":
            assert adapter.kernel_live is False


class TestIdempotencyEngine:
    """Emergency dispatch dedup - the Swytchcode governance signature."""

    def test_first_dispatch_succeeds(self, adapter):
        adapter._idempotency_cache.clear()
        res = adapter.dispatch_emergency_asha_alert(
            case_id="TEST-CASE-IDEM-001",
            priority="CRITICAL",
            clinical_condition="Test pre-eclampsia alert",
            vitals={"systolic_bp": 165, "diastolic_bp": 105},
            is_pregnant=True,
            gestational_weeks=32,
        )
        assert res["status"] == "DISPATCHED"
        assert res["idempotency_key"]

    def test_duplicate_dispatch_suppressed(self, adapter):
        adapter._idempotency_cache.clear()
        first = adapter.dispatch_emergency_asha_alert(
            case_id="TEST-CASE-IDEM-002",
            priority="CRITICAL",
            clinical_condition="Duplicate suppression test",
        )
        second = adapter.dispatch_emergency_asha_alert(
            case_id="TEST-CASE-IDEM-002",
            priority="CRITICAL",
            clinical_condition="Duplicate suppression test",
        )
        assert first["status"] == "DISPATCHED"
        assert second["status"] == "ALREADY_DISPATCHED_IDEMPOTENT"
        assert second["idempotency_hit"] is True


class TestVoiceGovernance:
    """Language policy enforcement for Indic voice calls."""

    def test_governed_language_approved(self, adapter):
        res = adapter.govern_voice_call("speech_to_text", "mr-IN", {"audio_len": 100})
        assert res["status"] == "GOVERNED_EXECUTION_APPROVED"

    def test_foreign_language_rejected(self, adapter):
        res = adapter.govern_voice_call("speech_to_text", "fr-FR", {})
        assert res["status"] == "POLICY_REJECTED"


class TestRouterEndpoints:
    """Swytchcode governance router surface for judges/demo."""

    @pytest.fixture()
    def client(self):
        from fastapi.testclient import TestClient
        from app.main import app
        return TestClient(app)

    def test_status_endpoint(self, client):
        r = client.get("/api/swytchcode/status")
        assert r.status_code == 200
        body = r.json()
        assert body["service"] == "Swytchcode AI Tool Execution & Governance"
        assert body["execution_path"] in ("NATIVE_RUNTIME_SDK", "CLOUD_API", "GOVERNOR_FALLBACK", "NONE")
        assert "sarvam_apis.translate.create" in body["tools_registered"]

    def test_manifest_endpoint(self, client):
        r = client.get("/api/swytchcode/manifest")
        assert r.status_code == 200
        body = r.json()
        assert "sarvam_apis.translate.create" in body.get("tools", {})

    def test_history_endpoint(self, client):
        r = client.get("/api/swytchcode/history")
        assert r.status_code == 200
        assert "history" in r.json()

    def test_execute_tool_translate_validation(self, client):
        r = client.post("/api/swytchcode/execute-tool", json={"tool_name": "sarvam_apis.translate.create"})
        assert r.status_code == 400  # 'text' required

    def test_execute_tool_unknown_blocked(self, client):
        r = client.post("/api/swytchcode/execute-tool", json={"tool_name": "malicious.unregistered.call"})
        assert r.status_code == 400  # allowlist enforcement
