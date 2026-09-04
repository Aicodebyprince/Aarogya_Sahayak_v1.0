# Swytchcode × Aarogya Sahayak: Governed AI Execution in Rural Healthcare

> **Hackathon Track**: AI Agent Tool Execution, API Governance & Developer Experience  
> **Project**: Aarogya Sahayak (AI-Powered Voice-First Rural Healthcare Platform for India)  
> **Sponsor Platform**: [Swytchcode (app.swytchcode.com)](https://app.swytchcode.com/dashboard/overview)  
> **Account**: `princesher321@gmail.com`

---

## Executive Summary

In rural Indian healthcare, when an AI assistant detects a life-threatening complication—such as a pregnant mother suffering from severe pre-eclampsia (BP 160/100 mmHg with blurred vision)—allowing an autonomous AI model to invoke external APIs directly is dangerous. Unchecked LLM tool calling leads to **hallucinated parameters, duplicate emergency dispatches, credential leaks, and zero auditability**.

By integrating **Swytchcode**, Aarogya Sahayak establishes an **enterprise-grade, zero-trust API Execution & Governance Runtime** that bridges:
1. **Multi-Agent Clinical Intelligence** (Google Gemini + Clinical Guideline RAG + Rule-Based Emergency Safety Engine)
2. **Sarvam AI Indic Voice Infrastructure** (Saaras Speech-to-Text & Bulbul Text-to-Speech across Hindi, Marathi, and regional dialects)
3. **Mission-Critical External APIs** (Emergency ASHA/Ambulance Notification Webhooks, ABDM Health Facility Registries, and Government Scheme Portals)

Swytchcode transforms fragile, unpredictable AI tool calls into **deterministic, idempotent, auditable, and secure transactions**.

---

## Key Value Pillars

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     SWYTCHCODE GOVERNANCE RUNTIME LAYER                          │
├───────────────────────┬─────────────────────────┬────────────────────────────────┤
│   ZERO-TOKEN EXPOSURE │  GUARANTEED IDEMPOTENCY │    SARVAM INDIC VOICE GATEWAY  │
│  LLMs never hold or   │  Emergency dispatches   │  Indic speech & translation    │
│  leak production API  │  execute exactly once;  │  runs with retry budgets &     │
│  keys or secrets.     │  deduplicates alerts.   │  PII scrubbing on weak 2G/3G.  │
├───────────────────────┼─────────────────────────┼────────────────────────────────┤
│   STRICT SCHEMA AUDIT │  LIVE OBSERVABILITY     │    DETERMINISTIC FALLBACK      │
│  Clinical parameters  │  Every execution shows  │  Zero hackathon demo crashes:  │
│  validated before any │  in real-time on the    │  graceful fallback to local    │
│  network dispatch.    │  Swytchcode dashboard.  │  verified clinical contracts.  │
└───────────────────────┴─────────────────────────┴────────────────────────────────┘
```

---

## Directory Index

This directory contains the complete Swytchcode integration documentation and execution assets:

| File | Description |
|---|---|
| [BEFORE_VS_AFTER.md](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/swytchcode/BEFORE_VS_AFTER.md) | In-depth breakdown of our architectural evolution: How we handled external integrations before vs. how Swytchcode solves it 10x better. |
| [INTEGRATION_ARCHITECTURE.md](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/swytchcode/INTEGRATION_ARCHITECTURE.md) | Technical blueprint detailing the Multi-Agent Orchestrator, Sarvam AI Voice Gateway, and Swytchcode Adapter flow. |
| [PITCH_AND_DEMO_GUIDE.md](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/swytchcode/PITCH_AND_DEMO_GUIDE.md) | 2-minute judge pitch script, live dashboard walkthrough on `app.swytchcode.com`, and judge Q&A preparation. |
| [tooling.json](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/swytchcode/tooling.json) | Production Swytchcode tool manifest defining schemas, policies, and retry bounds for all healthcare tools. |

---

## The 3 Core Tools Governed by Swytchcode

### 1. `dispatch_emergency_asha_alert`
* **Trigger**: Multi-Agent Triage detects high-risk maternal, pediatric, or cardiac danger signs.
* **Function**: Dispatches urgent triage alerts to the assigned village ASHA worker and PHC doctor queue.
* **Swytchcode Governance**: Enforces parameter schema validation (systolic/diastolic BP, SpO2, gestation week), generates unique idempotency keys to prevent duplicate ambulance dispatches, and logs latency and status to the Swytchcode dashboard.

### 2. `sarvam_indic_voice_gateway`
* **Trigger**: Citizen speaks symptoms in Marathi or Hindi via the mobile PWA.
* **Function**: Routes audio through Sarvam AI (Saaras STT / Bulbul TTS / Mayura Translate).
* **Swytchcode Governance**: Acts as a resilient proxy over intermittent rural networks, managing retries, timeout budgets, and rate limits without exposing Sarvam credentials to client code.

### 3. `query_health_facility_registry`
* **Trigger**: Patient or ASHA worker seeks the nearest facility capable of handling specific emergencies (e.g., ICU, Blood Bank, NICU).
* **Function**: Queries verified health facilities and Ayushman Bharat PM-JAY empanelled hospitals.
* **Swytchcode Governance**: Guarantees read-only execution; blocks any unauthorized database mutations while returning verified clinical capabilities.

---

## Quick Verification Command

To verify Swytchcode integration and connection status across the entire backend:

```bash
cd backend
python -m app.integrations.verify_all
```
