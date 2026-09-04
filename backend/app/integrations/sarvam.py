import requests
import logging
from typing import Dict, Any, Optional
from app.integrations.base import BaseIntegrationAdapter
from app.config import settings
from app.integrations.swytchcode import swytchcode_adapter

logger = logging.getLogger("aarogya-backend")

class SarvamAdapter(BaseIntegrationAdapter):
    """
    Sarvam AI Indic Voice, Speech-to-Text, Text-to-Speech & Translation Adapter.
    Governed by Swytchcode Runtime (Timeout enforcement, language policies, live telemetry).
    Supports Saaras (STT), Bulbul (TTS), and Mayura (Translate) models.
    """
    def __init__(self):
        super().__init__(mode=settings.SARVAM_MODE or "mock")
        self.api_key = settings.SARVAM_API_KEY
        self.base_url = "https://api.sarvam.ai"

    @property
    def is_mock(self) -> bool:
        return self.mode.lower() == "mock" or not self.api_key

    def speech_to_text(self, audio_bytes: bytes, filename: str = "audio.wav", language_code: str = "mr-IN") -> Dict[str, Any]:
        # Swytchcode Governance Hook
        gov_trace = swytchcode_adapter.govern_voice_call("speech_to_text", language_code, {"audio_len": len(audio_bytes) if audio_bytes else 0})
        if not audio_bytes or len(audio_bytes) == 0:
            return {
                "status": "NO_AUDIO",
                "transcript": "",
                "detected_language": language_code,
                "confidence": 0.0,
                "provider": "SARVAM"
            }

        if self.is_mock or not self.api_key:
            return {
                "status": "PROVIDER_UNAVAILABLE",
                "transcript": "",
                "detected_language": language_code,
                "confidence": 0.0,
                "provider": "SARVAM_UNCONFIGURED",
                "detail": "Sarvam API Key not configured or mode is mock"
            }

        try:
            url = f"{self.base_url}/speech-to-text"
            headers = {"api-subscription-key": self.api_key}
            files = {"file": (filename, audio_bytes, "audio/wav")}
            data = {"model": "saaras:v3", "language_code": language_code}

            resp = requests.post(url, headers=headers, files=files, data=data, timeout=15)
            if resp.status_code == 200:
                result = resp.json()
                return {
                    "status": "SUCCESS",
                    "transcript": result.get("transcript", ""),
                    "detected_language": result.get("language_code", language_code),
                    "confidence": result.get("trust_score", 0.95),
                    "provider": "SARVAM_LIVE"
                }
            else:
                return {
                    "status": "ERROR",
                    "error_code": f"HTTP_{resp.status_code}",
                    "detail": resp.text,
                    "transcript": "",
                    "provider": "SARVAM_LIVE"
                }
        except Exception as e:
            return {
                "status": "EXCEPTION",
                "detail": str(e),
                "transcript": "",
                "provider": "SARVAM_LIVE"
            }

    def text_to_speech(self, text: str, target_language_code: str = "mr-IN", speaker: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        # Swytchcode Governance Hook
        gov_trace = swytchcode_adapter.govern_voice_call("text_to_speech", target_language_code, {"text_len": len(text)})
        if not settings.SARVAM_TTS_ENABLED or self.is_mock or not self.api_key:
            return {
                "status": "PROVIDER_UNAVAILABLE",
                "audio_base64": None,
                "target_language": target_language_code,
                "provider": "SARVAM_UNAVAILABLE",
                "detail": "Sarvam API Key not configured or TTS disabled"
            }

        try:
            url = f"{self.base_url}/text-to-speech"
            headers = {
                "api-subscription-key": self.api_key,
                "Content-Type": "application/json"
            }
            selected_speaker = speaker or getattr(settings, "SARVAM_TTS_SPEAKER", "ritu")
            selected_model = model or getattr(settings, "SARVAM_TTS_MODEL", "bulbul:v3")

            payload = {
                "inputs": [text],
                "target_language_code": target_language_code,
                "speaker": selected_speaker,
                "model": selected_model
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                result = resp.json()
                audios = result.get("audios", [])
                base64_audio = audios[0] if audios else None
                return {
                    "status": "SUCCESS",
                    "audio_base64": base64_audio,
                    "target_language": target_language_code,
                    "provider": "SARVAM_LIVE"
                }
            else:
                return {
                    "status": "ERROR",
                    "error_code": f"HTTP_{resp.status_code}",
                    "detail": resp.text,
                    "provider": "SARVAM_FALLBACK"
                }
        except Exception as e:
            return {
                "status": "EXCEPTION",
                "detail": str(e),
                "provider": "SARVAM_FALLBACK"
            }

    def translate(self, text: str, source_language_code: str = "mr-IN", target_language_code: str = "en-IN") -> Dict[str, Any]:
        if self.is_mock or not self.api_key:
            return {
                "status": "MOCKED",
                "translated_text": text,
                "provider": "SARVAM_MOCK"
            }

        # Swytchcode Kernel Path: execute translation through the governed kernel
        # (sarvam_apis.translate.create) with validation, retries, and audit.
        if swytchcode_adapter.kernel_live:
            kernel_result = swytchcode_adapter.exec_translate(
                text=text,
                source_language_code=source_language_code,
                target_language_code=target_language_code,
            )
            if kernel_result.get("status") == "SUCCESS":
                return {
                    "status": "SUCCESS",
                    "translated_text": kernel_result.get("translated_text", text),
                    "provider": "SARVAM_VIA_SWYTCHCODE",
                    "swytchcode_trace": kernel_result.get("trace"),
                }
            logger.warning(
                f"[Sarvam] Swytchcode kernel translate failed ({kernel_result.get('status')}), "
                f"falling back to direct call."
            )

        try:
            url = f"{self.base_url}/translate"
            headers = {
                "api-subscription-key": self.api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "input": text,
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
                "speaker_gender": "Female",
                "mode": "formal",
                "model": "mayura:v1"
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                result = resp.json()
                return {
                    "status": "SUCCESS",
                    "translated_text": result.get("translated_text", text),
                    "provider": "SARVAM_LIVE"
                }
            else:
                return {
                    "status": "ERROR",
                    "translated_text": text,
                    "provider": "SARVAM_FALLBACK"
                }
        except Exception as e:
            return {
                "status": "EXCEPTION",
                "translated_text": text,
                "provider": "SARVAM_FALLBACK"
            }

sarvam_adapter = SarvamAdapter()
