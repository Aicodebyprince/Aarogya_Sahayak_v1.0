from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

from app.integrations.lyzr import lyzr_adapter

router = APIRouter(prefix="/lyzr", tags=["Lyzr AI Agent Multi-Agent Mesh"])

class LyzrTriageRequest(BaseModel):
    symptoms: str = Field(..., description="Conversational symptoms or patient complaint")
    is_pregnant: Optional[bool] = Field(default=False, description="Whether the patient is pregnant")
    gestational_weeks: Optional[int] = Field(default=None, description="Gestational weeks if pregnant")
    systolic_bp: Optional[int] = Field(default=None, description="Systolic Blood Pressure (mmHg)")
    diastolic_bp: Optional[int] = Field(default=None, description="Diastolic Blood Pressure (mmHg)")
    spo2: Optional[int] = Field(default=None, description="Oxygen Saturation SpO2 (%)")
    temperature_c: Optional[float] = Field(default=None, description="Body Temperature (°C)")
    session_id: Optional[str] = Field(default=None, description="Optional custom session identifier")

class LyzrSchemeRequest(BaseModel):
    is_pregnant: Optional[bool] = Field(default=True, description="Whether patient is pregnant")
    rural: Optional[bool] = Field(default=True, description="Whether citizen is located in a rural village")

@router.get("/status")
def get_lyzr_status() -> Dict[str, Any]:
    """
    Returns the live health, connectivity, and configuration of all 4 deployed Lyzr Agents.
    """
    return lyzr_adapter.get_status()

@router.get("/agents")
def list_lyzr_agents() -> Dict[str, Any]:
    """
    Lists the 4 specialized agents in the Lyzr Multi-Agent Consensus Mesh.
    """
    status_info = lyzr_adapter.get_status()
    return {
        "platform": "Lyzr AI Studio Multi-Agent Mesh",
        "mode": status_info["mode"],
        "total_agents": 4,
        "mesh_topology": status_info["mesh_topology"],
        "governance": status_info["governance"]
    }

@router.post("/triage")
def execute_lyzr_triage(request: LyzrTriageRequest) -> Dict[str, Any]:
    """
    Executes clinical and welfare triage through the deployed Lyzr Manager Agent ('Aarogya Clinical Navigator')
    audited by the Medical Safety Guardrail Agent.
    """
    result = lyzr_adapter.route_and_triage(
        normalized_text=request.symptoms,
        is_pregnant=request.is_pregnant or False,
        gestational_weeks=request.gestational_weeks,
        systolic_bp=request.systolic_bp,
        diastolic_bp=request.diastolic_bp,
        spo2=request.spo2,
        temperature_c=request.temperature_c,
        session_id=request.session_id
    )
    return result

@router.post("/schemes")
def execute_lyzr_schemes(request: LyzrSchemeRequest) -> Dict[str, Any]:
    """
    Directly queries Agent 3 ('Aarogya Welfare Schemes Agent') on Lyzr Studio for Indian welfare entitlements.
    """
    return lyzr_adapter.evaluate_schemes(
        is_pregnant=request.is_pregnant,
        rural=request.rural
    )
