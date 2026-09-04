# Aarogya Sahayak × Swytchcode: Complete Live Verification & Demonstration Playbook

> **Target Audience**: Hackathon Judges, Evaluators & Technical Mentors  
> **Sponsor Platform**: [Swytchcode (app.swytchcode.com)](https://app.swytchcode.com/dashboard/overview)  
> **Registered Account**: `princesher321@gmail.com`  
> **CLI Workspace**: `calm-meadow-c150` (`85ab6d86-dd8c-41f2-ad8d-f310d3cfa936`)  
> **Printable PDF Presentation**: [SWYTCHCODE_INTEGRATION_SHOWCASE.html](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/swytchcode/SWYTCHCODE_INTEGRATION_SHOWCASE.html) *(Open in Chrome/Edge and press Ctrl+P to save as PDF)*

---

## 1. System Architecture Blueprint

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CITIZEN MOBILE PWA (React / Vite)                     │
│  [UI Banner: "🛡️ Swytchcode AI Runtime: Governed & Idempotent (Telemetry ↗)"]│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTPS (Audio / Symptoms)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AAROGYA SAHAYAK FASTAPI BACKEND (Render)                 │
│                                                                             │
│   ┌────────────────────────┐                   ┌────────────────────────┐   │
│   │ Deterministic Triage   │                   │  PII Masking Engine    │   │
│   │ (Rule-Based Evaluator) │                   │  (Anonymizes Vitals)   │   │
│   └───────────┬────────────┘                   └───────────┬────────────┘   │
│               └──────────────────────┬─────────────────────┘                │
│                                      ▼                                      │
│                      SWYTCHCODE INTEGRATION ADAPTER                         │
│                 (backend/app/integrations/swytchcode.py)                    │
│                                                                             │
│    • Ingress Schema Validation       • SHA-256 Idempotency Deduplication    │
│    • Zero-Token Credential Vault     • Local Fallback Invariant (Zero Crash)│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Governed Tool Dispatch
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│               SWYTCHCODE CLOUD & DASHBOARD (app.swytchcode.com)              │
│                 Telemetry • Latency • Policies • Real-time Events           │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
                       ▼                               ▼
       ┌───────────────────────────────┐ ┌──────────────────────────────┐
       │     SARVAM AI INDIC VOICE     │ │   EMERGENCY ASHA DISPATCH    │
       │   - Saaras (Speech-to-Text)   │ │   - Urgent Triage Webhook    │
       │   - Bulbul (Text-to-Speech)   │ │   - Deduplicated 1x Delivery │
       │   - Governed Latency Budget   │ │   - Zero Patient PII Leaked  │
       └───────────────────────────────┘ └──────────────────────────────┘
```

---

## 2. How to Check What Is Working (Live Verification Steps)

You can run these checks either locally or against your live Render backend URL.

### Test 1: Check Swytchcode Runtime Health & Registered Tools
Ping the `/api/swytchcode/status` endpoint:

```bash
# Against local backend:
curl -X GET "http://localhost:8000/api/swytchcode/status"

# Against live Render backend:
curl -X GET "https://your-backend.onrender.com/api/swytchcode/status"
```

**Expected JSON Response (Live Proof)**:
```json
{
  "service": "Swytchcode AI Tool Execution & Governance",
  "status": "LIVE_CONNECTED",
  "mode": "LIVE",
  "live_connected": true,
  "account": "princesher321@gmail.com",
  "workspace_alias": "calm-meadow-c150",
  "workspace_uuid": "85ab6d86-dd8c-41f2-ad8d-f310d3cfa936",
  "cli_workspace_linked": true,
  "installed_integrations": ["Gemini.gemini", "Sarvam ai.sarvam_apis"],
  "tools_registered": [
    "dispatch_emergency_asha_alert",
    "sarvam_indic_voice_gateway",
    "query_health_facility_registry"
  ],
  "governance_policies": {
    "zero_token_exposure": "ENFORCED",
    "idempotency": "ENFORCED",
    "schema_validation": "ENFORCED",
    "sarvam_voice_proxy": "ACTIVE",
    "db_write_isolation": "ENFORCED"
  }
}
```

---

### Test 2: Execute Live Governed Emergency Triage Alert
Trigger a simulated emergency maternal alert:

```bash
curl -X POST "http://localhost:8000/api/swytchcode/execute-tool" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "dispatch_emergency_asha_alert",
    "case_id": "HACKATHON-DEMO-01",
    "priority": "CRITICAL",
    "clinical_condition": "Severe pre-eclampsia: BP 165/105 mmHg with blurred vision",
    "systolic_bp": 165,
    "diastolic_bp": 105,
    "spo2": 97,
    "is_pregnant": true,
    "gestational_weeks": 32
  }'
```

**Expected JSON Response**:
```json
{
  "status": "DISPATCHED",
  "provider": "SWYTCHCODE_LIVE",
  "trace_id": "SWY-EMG-C0E4A3D2",
  "idempotency_key": "9f83a4...",
  "case_id": "HACKATHON-DEMO-01",
  "priority": "CRITICAL",
  "clinical_condition": "Severe pre-eclampsia: BP 165/105 mmHg with blurred vision",
  "latency_ms": 135.2,
  "governance": {
    "zero_token_exposure": true,
    "schema_validated": true,
    "idempotency_enforced": true,
    "pii_scrubbed": true
  },
  "dashboard_audit_url": "https://app.swytchcode.com/dashboard/overview"
}
```

---

### Test 3: The Idempotency Test (Show Duplicate Suppression)
Run the **exact same `curl` command a second time**.

**Expected JSON Response**:
```json
{
  "status": "ALREADY_DISPATCHED_IDEMPOTENT",
  "idempotency_hit": true,
  "message": "Duplicate emergency alert suppressed by Swytchcode idempotency engine.",
  "trace_id": "SWY-EMG-C0E4A3D2"
}
```
> **What to tell judges**:  
> *"Notice how the second call was deduplicated instantly. In a remote village where cell signals disconnect mid-flight, this prevents five ambulances from being dispatched to the same house."*

---

### Test 4: Comprehensive Truth Verification Report
Run the built-in system audit script:

```bash
cd backend
.venv\Scripts\python -m app.integrations.verify_all
```

**Output**:
```text
======================================================================
   Aarogya Sahayak - Comprehensive Live Integration Truth Report
======================================================================

TECHNOLOGY / ADAPTER           | MODE       | STATUS                   | DETAILS
---------------------------------------------------------------------------------------------------------
Milvus Clinical RAG            | FALLBACK   | LOCAL_SERVICE_VERIFIED   | 19 clinical guideline chunks indexed
Neo4j Scheme GraphRAG          | FALLBACK   | LOCAL_SERVICE_VERIFIED   | Deterministic Cypher-equivalent graph traversal
Google Gemini (google-genai)   | FALLBACK   | BLOCKED_BY_CREDENTIALS   | Pydantic structured output contracts active
Lyzr Multi-Agent Orchestrator  | LOCAL_FALLBACK | LOCAL_SERVICE_VERIFIED | 4-agent execution sequence passing
Sarvam Voice STT/TTS           | MOCK       | BLOCKED_BY_CREDENTIALS   | Sarvam ASR Marathi/Hindi speech translator active
n8n Workflow Automation        | LIVE       | LOCAL_SERVICE_VERIFIED   | HMAC SHA-256 webhook dispatcher operational
Swytchcode AI Tool Execution   | LIVE       | LIVE_CONNECTED           | Account: princesher321@gmail.com; Governs ASHA dispatch, Sarvam Voice & Idempotency
```

---

## 3. The 3-Minute Live Demo Walkthrough (For the Judges)

Follow this exact sequence on stage:

### Step 1: Open 3 Browser Tabs
1. **Tab 1**: Citizen Mobile PWA (`http://localhost:5173` or live Vercel URL).
2. **Tab 2**: Swytchcode Dashboard (`https://app.swytchcode.com/dashboard/overview`).
3. **Tab 3**: Printable Architecture Showcase ([`swytchcode/SWYTCHCODE_INTEGRATION_SHOWCASE.html`](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/swytchcode/SWYTCHCODE_INTEGRATION_SHOWCASE.html)).

### Step 2: Trigger the Emergency Voice Flow in Tab 1
* Click the microphone or type:  
  `"Pregnant 32 weeks, severe headache, blurred vision, BP 160/100"`
* Point to the top banner:  
  `🛡️ Swytchcode AI Runtime: Governed & Idempotent — Live Telemetry ↗`
* Show how the AI immediately flagged **Critical Pre-eclampsia** and initiated governed ASHA dispatch.

### Step 3: Switch to Tab 2 (Swytchcode Dashboard)
* Show the live telemetry stream:
  * **Tool**: `dispatch_emergency_asha_alert`
  * **Status**: `200 OK`
  * **Trace ID**: Matching the ID displayed in the app
  * **Account**: `princesher321@gmail.com`
* Say: *"Here is the live proof. The LLM never held an API key. Swytchcode validated the clinical schema, isolated patient PII, and enforced an idempotency lock before touching the network."*

---

## 4. How to Generate / Print the PDF Presentation

1. Double-click or open in Chrome/Edge:
   `swytchcode/SWYTCHCODE_INTEGRATION_SHOWCASE.html`
2. Press **`Ctrl + P`** (Print).
3. Under Destination, select **`Save as PDF`**.
4. Check **Background graphics** (ON).
5. Click **Save** → Save as `AarogyaSahayak_Swytchcode_Architecture.pdf`.

You now have an executive, beautifully formatted PDF ready for submission!
