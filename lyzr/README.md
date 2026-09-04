# Lyzr AI × Aarogya Sahayak: 4-Agent Consensus Mesh for Rural Indian Healthcare

> **Hackathon Track**: Enterprise Multi-Agent Mesh, Clinical Safety Governance & Social Welfare Intelligence  
> **Project**: Aarogya Sahayak (AI-Powered Voice-First Rural Healthcare Platform for India)  
> **Sponsor Platform**: [Lyzr AI Studio (studio.lyzr.ai)](https://studio.lyzr.ai/)  
> **Live Agents Deployed**: 4 Autonomous Agents (Manager, Guardrail, Schemes, Protocols)  
> **Deployment**: Production & Staging (Render Singapore + Vercel)

---

## 1. Executive Summary

In rural Indian healthcare, frontline Community Health Workers (ASHAs) handle primary triage for over 800 million citizens. When assessing a high-risk patient—such as a 28-week pregnant mother suffering from severe pre-eclampsia (BP 160/100 mmHg with blurred vision and headache)—a single monolithic LLM prompt is prone to **hallucination, missed maternal red flags, unauthorized drug prescribing, and lack of protocol citations**.

By integrating **Lyzr AI Studio**, Aarogya Sahayak implements a **4-Agent Consensus Mesh** where specialized autonomous agents collaborate under strict clinical and safety constraints:

1. **Manager Agent (`Aarogya Clinical Navigator`)**: Ingests patient symptoms & vitals, coordinates clinical assessment, and delegates to the medical safety guardrail.
2. **Medical Safety Guardrail Agent (`Aarogya Safety Guardrail`)**: Six-Sigma Clinical Auditor with **absolute veto power**; blocks unauthorized drug prescribing and mandates emergency physical referral.
3. **Welfare Schemes Specialist (`Aarogya Welfare Schemes`)**: Evaluates direct benefit entitlements under **Janani Suraksha Yojana (JSY: ₹1,400)**, **PMMVY (₹5,000 DBT)**, and **Ayushman Bharat PM-JAY (₹5,00,000 cover)**.
4. **Clinical Protocol Agent (`Aarogya Clinical Protocol`)**: Grounds medical assessments strictly in official **MoHFW** maternal care manuals and **ICMR Standard Treatment Workflows**.

---

## 2. Deployed Lyzr Multi-Agent Specification

| Agent Name | Lyzr Live Agent ID | Model | Core Mandate & Responsibility |
|---|---|---|---|
| **1. Manager Agent** (`Aarogya Clinical Navigator`) | `6a9ae0e14a372650b843a9ae` | OpenAI `gpt-4o` | Central triage coordinator; delegates to safety guardrail sub-agent |
| **2. Medical Safety Guardrail** (`Aarogya Safety Guardrail`) | `6a9ae9404e6f909d5b1ce8e7` | OpenAI `gpt-4o` | Six-Sigma Medical Auditor with absolute veto power |
| **3. Welfare Schemes Specialist** (`Aarogya Welfare Schemes`) | `6a9aeb88f70815409cbca57f` | OpenAI `gpt-4o` | Calculates JSY, PMMVY, and PM-JAY cash and insurance entitlements |
| **4. Clinical Protocol Agent** (`Aarogya Clinical Protocol`) | `6a9aec908d69d22325c3e67f` | OpenAI `gpt-5.4-mini` | ICMR Standard Treatment Workflows & MoHFW protocol grounding |

---

## 3. System Architecture: Lyzr + Swytchcode Synergy

```
+-----------------------------------------------------------------------------------+
|                           CITIZEN / ASHA VOICE INPUT                              |
|                    (Hindi / Marathi Speech via Sarvam Voice)                      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        THE BRAIN: LYZR 4-AGENT MESH                               |
|                                                                                   |
|  [Manager Agent: Clinical Navigator] (ID: 6a9ae0e14a372650b843a9ae)               |
|      |                                                                            |
|      +---> [Agent 4: ICMR Protocol RAG] (ID: 6a9aec908d69d22325c3e67f)            |
|      |                                                                            |
|      +---> [Agent 3: Welfare Schemes] (ID: 6a9aeb88f70815409cbca57f)              |
|      |                                                                            |
|      v                                                                            |
|  [Agent 2: Medical Safety Guardrail & Veto] (ID: 6a9ae9404e6f909d5b1ce8e7)         |
|      * Vetoes unauthorized prescription drugs                                     |
|      * Enforces immediate PHC escalation for maternal emergencies                  |
+-----------------------------------------------------------------------------------+
                                         |
                       Structured Escalation Directive
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        THE HAND: SWYTCHCODE RUNTIME                               |
|                  (Zero-Trust API Execution & Tool Governance)                     |
|                                                                                   |
|  * Computes SHA-256 Sliding-Window Idempotency Hash                               |
|  * Dispatches Governed Emergency ASHA Alert Webhook & Sarvam Voice Call            |
+-----------------------------------------------------------------------------------+
```

- **Lyzr AI is the Brain**: Multi-agent reasoning, clinical guideline citations, scheme entitlement calculation, and safety vetoes.
- **Swytchcode is the Hand**: Zero-trust API execution, deduplication of emergency dispatches, and voice gateway proxying.

---

## 4. API Endpoints

### 1. Lyzr Mesh Health & Topology
```http
GET /api/lyzr/status
GET /api/lyzr/agents
```
Returns live connection status, active models, and the 4-agent topology.

### 2. Live Clinical & Scheme Triage
```http
POST /api/lyzr/triage
Content-Type: application/json

{
  "symptoms": "Pregnant 28 weeks, severe throbbing headache, blurred vision",
  "is_pregnant": true,
  "gestational_weeks": 28,
  "systolic_bp": 160,
  "diastolic_bp": 100
}
```

### 3. Direct Welfare Schemes Consultation
```http
POST /api/lyzr/schemes
Content-Type: application/json

{
  "is_pregnant": true,
  "rural": true
}
```
Directly queries Agent 3 (`Aarogya Welfare Schemes Agent`) on Lyzr Studio.
