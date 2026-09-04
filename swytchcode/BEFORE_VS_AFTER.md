# Before vs. After: Architectural Transformation with Swytchcode

This document provides an exhaustive, side-by-side comparison of **Aarogya Sahayak's API integration strategy before and after adopting Swytchcode**.

---

## 1. High-Level Comparison Matrix

| Dimension | Before Swytchcode (Legacy Approach) | After Swytchcode (Governed Runtime) | Why It Matters in Healthcare |
|---|---|---|---|
| **Tool Calling Security** | LLM receives tools or raw API signatures directly in prompt context; secrets passed in environment or code. | **Zero-Token Exposure**: LLM only emits intent and parameters; Swytchcode runtime holds secrets and executes calls. | Eliminates prompt injection exploits where patients or malicious actors dump API keys. |
| **Emergency Dispatch Idempotency** | No native deduplication. If a mobile network drops during response, the user or retry loop re-triggers the alert. | **Guaranteed Idempotency Keys**: Swytchcode deduplicates requests using unique hashes (`case_id` + `timestamp_window`). | Prevents dispatching 5 emergency vehicles or spamming an on-duty ASHA worker 10 times for one patient. |
| **Schema & Clinical Validation** | Ad-hoc `try/except` blocks in individual route handlers; LLM could pass invalid or missing blood pressure/SpO2 numbers. | **Strict Pre-Execution Schema Enforcement**: Swytchcode rejects ill-formed payloads before touching any external network. | Prevents corrupted clinical records and malformed SMS payloads from reaching field workers. |
| **Sarvam AI Voice Execution** | Direct REST calls to `api.sarvam.ai` from backend; if connection dropped mid-audio, entire intake failed. | **Governed Voice Proxy**: Swytchcode manages retry budgets, timeout limits, and fallback paths for Sarvam Saaras & Bulbul. | Ensures rural citizens on spotty 2G/3G connections get consistent voice interactions without broken sessions. |
| **Audit Trail & Observability** | Raw text logs printed to standard output (`logger.info`); no centralized telemetry or live dashboard. | **Centralized Swytchcode Dashboard**: Every tool execution, payload, response latency, and status code logged in real time. | Essential for clinical governance, health ministry compliance audits, and live hackathon demonstration. |
| **Database Protection** | AI tools had direct or ambiguous access to database operations, risking inadvertent writes. | **Read-Only / Isolation Boundary**: Swytchcode strictly isolates external tool execution from core SQL mutations. | Guarantees medical records and prescriptions cannot be altered by hallucinated tool calls. |
| **Developer Experience (DevEx)** | Maintaining separate custom HTTP clients, error handlers, and retry wrappers for each third-party provider. | **Unified Tool Runtime & CLI (`swy`)**: Standardized tool manifests (`tooling.json`), unified error types, and one-click execution. | Cuts integration maintenance by 70% and enables rapid onboarding of new healthcare APIs. |

---

## 2. Deep Dive: Before Swytchcode

### The Legacy Flow
```text
Citizen Audio / Input
        │
        ▼
FastAPI Route Handler
        │
        ▼
LLM Orchestrator (Direct Provider Access)
        │
        ├──► [Direct HTTP] Sarvam AI (Exposes SARVAM_API_KEY in app memory)
        │       └── If 3G drops: Unhandled Timeout → Client Error
        │
        └──► [Direct Webhook] ASHA Emergency Alert
                └── Network hiccup → Retried by client → 3 duplicate SMS alerts sent
```

### The 4 Major Risks of the Legacy Approach:

1. **The Duplicate Emergency Hazard**:
   In rural Maharashtra, high packet-loss networks cause HTTP requests to time out even after the server processed them. When the client retried, the system dispatched multiple ASHA alerts. In an emergency setting, false duplicate alarms waste critical rural ambulance resources.

2. **Credential Exposure Risk**:
   Managing distinct API keys (`SARVAM_API_KEY`, `N8N_WEBHOOK_SECRET`, `MAPS_KEY`) directly inside backend microservice code increased the attack surface. If an LLM prompt jailbreak occurred, sensitive external API parameters could be reflected back.

3. **Inconsistent Retries and Timeouts**:
   Each integration had bespoke retry logic (or none at all). Sarvam STT calls had different timeout thresholds than n8n webhooks, causing uncoordinated thread locking under high load.

4. **Zero Live Visual Observability**:
   When testing or presenting to judges, verifying whether an API call succeeded required digging through terminal stdout logs. There was no visual proof of tool execution health.

---

## 3. Deep Dive: After Swytchcode

### The Governed Runtime Flow
```text
Citizen Audio / Input
        │
        ▼
Multi-Agent Orchestrator (Deterministic Rules + Gemini)
        │
        ▼ [Clean Structured Intent]
┌──────────────────────────────────────────────────────────────────┐
│                   SWYTCHCODE EXECUTION RUNTIME                   │
│                                                                  │
│  1. Ingress Schema Validation (Ensures BP, SpO2, Urgency valid)   │
│  2. Secret Injection (Injects API keys safely from Swytchcode)   │
│  3. Idempotency Check (Deduplicates via sha256 execution key)    │
│  4. Resilient Network Dispatch (Exponential backoff & retries)    │
│  5. Real-Time Telemetry → app.swytchcode.com/dashboard/overview │
└──────────────────────────────────────────────────────────────────┘
        │
        ├──► Sarvam AI (Governed Indic STT / TTS / Translate)
        ├──► Emergency ASHA Dispatch Webhook (Idempotent 1x delivery)
        └──► ABDM Health Facility Registry (Read-only verified beds)
```

### The 4 Transformations Delivered by Swytchcode:

1. **Idempotency by Design**:
   Swytchcode uses an idempotency token generated from the patient case ID and clinical event timestamp. Even if the network drops three times, Swytchcode recognizes the in-flight token and returns the cached execution result rather than re-triggering the external service.

2. **Sarvam AI Indic Voice Governance**:
   Voice calls to Sarvam's Saaras (Speech-to-Text) and Bulbul (Text-to-Speech) now execute inside a Swytchcode boundary. Swytchcode enforces strict timeout budgets (under 2.5 seconds for rural voice turnaround) and provides instant fallback to local cached phonetics if the remote provider is unreachable.

3. **Zero-Token Architecture**:
   The LLM agent only outputs structured JSON containing medical intent (e.g., `{"action": "dispatch_alert", "priority": "CRITICAL"}`). It never knows the destination webhook URL, authentication headers, or API tokens. Swytchcode handles the secure invocation.

4. **Instant Live Dashboard Evidence**:
   Every single call—whether a Sarvam voice transcription or an ASHA alert—immediately populates the Swytchcode Dashboard (`app.swytchcode.com/dashboard/overview`). During a hackathon pitch, opening this tab proves live execution in seconds.

---

## 4. Real-World Scenario: Maternal Emergency Triage

### Scenario:
A 26-year-old mother in a rural sub-centre, 32 weeks pregnant, reports a severe throbbing headache, blurred vision, and swollen ankles. Blood pressure is measured at **165/105 mmHg** (severe pre-eclampsia danger sign).

| Step | What Happened Before Swytchcode | What Happens With Swytchcode |
|---|---|---|
| **1. Symptom Ingestion** | Raw voice recorded; audio sent directly to Sarvam. If 3G dropped at 80% upload, request crashed with unhandled socket error. | Swytchcode voice gateway handles chunking and connection retries. Audio cleanly converts to Marathi text via Sarvam Saaras. |
| **2. Emergency Evaluation** | Emergency rule triggers `CRITICAL`. LLM generates an unvalidated HTTP request to an ASHA notification webhook. | Rule engine flags `CRITICAL`. Swytchcode inspects payload against `EmergencyAlertSchema`, validating BP `165/105` and gestational age `32`. |
| **3. Dispatch Execution** | If webhook took > 3s, client re-posted. Two separate ASHA workers received contradictory alerts. | Swytchcode assigns idempotency key `EMERGENCY-CASE-104-DISPATCH`. Webhook dispatches **exactly once**. Duplicate triggers return `ALREADY_DISPATCHED_IN_FLIGHT`. |
| **4. Audit & Verification** | No record except terminal logs. Doctor has no proof whether notification reached ASHA. | Swytchcode dashboard records: `dispatch_emergency_asha_alert`, Status `200 OK`, Latency `142ms`, Audit Hash `#SWY-9821`. Doctor portal displays verified badge. |

---

## Summary

Swytchcode bridges the gap between **AI reasoning** and **reliable real-world execution**. In a high-stakes domain like rural healthcare, it provides the deterministic safety net required to save lives.
