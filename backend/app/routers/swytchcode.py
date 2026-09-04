import os
import json
from fastapi import APIRouter, HTTPException, Query, status
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.integrations.swytchcode import swytchcode_adapter

router = APIRouter(prefix="/swytchcode", tags=["Swytchcode AI Tool Governance"])

class ToolExecutionRequest(BaseModel):
    tool_name: str
    case_id: Optional[str] = "CASE-DEMO-001"
    priority: Optional[str] = "CRITICAL"
    clinical_condition: Optional[str] = "Maternal pre-eclampsia danger sign: BP 165/105 mmHg with blurred vision"
    systolic_bp: Optional[int] = 165
    diastolic_bp: Optional[int] = 105
    spo2: Optional[int] = 97
    is_pregnant: Optional[bool] = True
    gestational_weeks: Optional[int] = 32
    language_code: Optional[str] = "mr-IN"
    text: Optional[str] = None
    source_language_code: Optional[str] = "en-IN"
    target_language_code: Optional[str] = "hi-IN"
    prompt: Optional[str] = None

@router.get("/status")
def get_swytchcode_status() -> Dict[str, Any]:
    """
    Returns live Swytchcode runtime connection status, policies, and telemetry.
    """
    return swytchcode_adapter.get_status()

@router.post("/execute-tool")
def execute_swytchcode_tool(request: ToolExecutionRequest) -> Dict[str, Any]:
    """
    Directly executes a governed tool through Swytchcode.
    Useful for live hackathon demonstration to judges and automated testing.
    """
    if request.tool_name == "dispatch_emergency_asha_alert":
        return swytchcode_adapter.dispatch_emergency_asha_alert(
            case_id=request.case_id or "CASE-DEMO-001",
            priority=request.priority or "CRITICAL",
            clinical_condition=request.clinical_condition or "Severe pre-eclampsia alert",
            vitals={
                "systolic_bp": request.systolic_bp,
                "diastolic_bp": request.diastolic_bp,
                "spo2": request.spo2
            },
            is_pregnant=request.is_pregnant or False,
            gestational_weeks=request.gestational_weeks,
            assigned_asha_id="ASHA-KLN-04"
        )
    elif request.tool_name == "sarvam_indic_voice_gateway":
        return swytchcode_adapter.govern_voice_call(
            operation="speech_to_text",
            language_code=request.language_code or "mr-IN",
            payload_details={"sample_audio": True}
        )
    elif request.tool_name == "query_health_facility_registry":
        return swytchcode_adapter.query_health_facility_registry(
            latitude=19.8762,
            longitude=75.3433,
            required_capability="24x7_emergency"
        )
    elif request.tool_name == "sarvam_apis.translate.create":
        if not request.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'text' is required for translate"
            )
        return swytchcode_adapter.exec_translate(
            text=request.text,
            source_language_code=request.source_language_code or "en-IN",
            target_language_code=request.target_language_code or "hi-IN",
        )
    elif request.tool_name == "sarvam_apis.transliterate.create":
        if not request.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'text' is required for transliterate"
            )
        return swytchcode_adapter.exec_transliterate(
            text=request.text,
            source_language_code=request.source_language_code or "en-IN",
            target_language_code=request.target_language_code or "hi-IN",
        )
    elif request.tool_name == "sarvam_apis.stream.create":
        if not request.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'text' is required for tts stream"
            )
        return swytchcode_adapter.exec_tts_stream(
            text=request.text,
            target_language_code=request.target_language_code or "hi-IN",
        )
    elif request.tool_name == "gemini.model.modelgenerateContent.create":
        if not request.prompt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'prompt' is required for gemini generation"
            )
        return swytchcode_adapter.exec_gemini_generate(prompt=request.prompt)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tool '{request.tool_name}' not registered in Swytchcode tooling manifest."
        )

@router.get("/history")
def get_execution_history() -> Dict[str, Any]:
    """
    Returns recent tool executions logged in Swytchcode runtime.
    """
    return {
        "count": len(swytchcode_adapter._execution_history),
        "history": list(reversed(swytchcode_adapter._execution_history))
    }

@router.get("/manifest")
def get_tooling_manifest() -> Dict[str, Any]:
    """
    Returns Swytchcode tooling.json configuration manifest.
    """
    backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    manifest_path = os.path.join(backend_root, ".swytchcode", "tooling.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "project": "aarogya-sahayak",
        "status": "MANIFEST_NOT_FOUND",
        "tools": [
            "dispatch_emergency_asha_alert",
            "sarvam_indic_voice_gateway",
            "query_health_facility_registry"
        ]
    }
