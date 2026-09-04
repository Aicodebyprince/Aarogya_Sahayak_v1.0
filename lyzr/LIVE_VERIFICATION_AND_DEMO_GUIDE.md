# Lyzr AI: Live Verification & Stage Pitch Guide

> **Live Agent**: `Aarogya Clinical Navigator` (ID: `6a9ae0e14a372650b843a9ae`)  
> **Backend Base URL**: `http://localhost:8000/api` (or Render production URL)

---

## 1. Quick Verification Commands

### Check Lyzr Connection & Health Status
```bash
curl -X GET "http://localhost:8000/api/lyzr/status"
```
**Expected Response**:
```json
{
  "service": "Lyzr AI Agent Studio",
  "agent_id": "6a9ae0e14a372650b843a9ae",
  "agent_name": "Aarogya Clinical Navigator",
  "mode": "LIVE",
  "endpoint": "https://agent-prod.studio.lyzr.ai/v3/inference/chat/",
  "provider_model": "OpenAI gpt-4o (Lyzr-managed)",
  "api_key_configured": true,
  "guardrails_active": true,
  "consensus_mesh": [
    "1. Lyzr Triage Intake Agent",
    "2. Lyzr ICMR/MoHFW Clinical Protocol RAG Agent",
    "3. Lyzr Indian Welfare Scheme Agent",
    "4. Lyzr Six-Sigma Medical Safety Critic (Veto Guardrail)"
  ]
}
```

---

### Run Live Maternal Emergency Triage via Lyzr Agent
```bash
curl -X POST "http://localhost:8000/api/lyzr/triage" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "Pregnant mother 28 weeks with throbbing headache, blurred vision, swelling in feet",
    "is_pregnant": true,
    "gestational_weeks": 28,
    "systolic_bp": 160,
    "diastolic_bp": 100
  }'
```
**Expected Response**:
- `status`: `"LIVE"`
- `provider`: `"Lyzr AI Studio (Aarogya Clinical Navigator)"`
- `triage_urgency`: `"CRITICAL"`
- `danger_signs`: `["Severe headache", "Blurred vision", "Pre-eclampsia danger sign"]`
- `guideline_citations`: `["MoHFW: Management of Hypertensive Disorders in Pregnancy"]`
- `eligible_schemes`: `["Janani Suraksha Yojana (JSY)", "Pradhan Mantri Matru Vandana Yojana (PMMVY)"]`
- `verifier_approved`: `true`

---

## 2. Live Demo Script for Judges (60-Second Walkthrough)

1. **The Hook (15s)**:
   > *"In rural India, an AI assistant cannot simply be a generic chatbot. If a pregnant mother reports severe headache with BP 160/100, hallucinating a prescription or missing pre-eclampsia is fatal."*

2. **The Solution (25s)**:
   > *"We deployed our custom agent 'Aarogya Clinical Navigator' directly on **Lyzr AI Studio**. Powered by Lyzr's multi-agent architecture and gpt-4o, it analyzes vitals, checks ICMR maternal protocols, identifies government scheme entitlements like JSY and PMMVY, and enforces a Six-Sigma medical safety veto."*

3. **The Proof & Synergy (20s)**:
   > *"Watch this live: Lyzr's multi-agent consensus flags the pregnancy emergency as CRITICAL in real time, and immediately hands off the structured alert to **Swytchcode**, which safely and idempotently notifies the local ASHA worker with zero duplicate ambulance calls."*
