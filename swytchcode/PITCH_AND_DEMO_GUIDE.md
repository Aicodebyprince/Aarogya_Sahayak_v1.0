# Swytchcode Hackathon Pitch & Live Demo Guide

Use this playbook to deliver a high-impact, 2-minute pitch to the hackathon judges and showcase your live Swytchcode integration.

---

## 1. The 2-Minute Winning Pitch Script

### [0:00 - 0:30] The High-Stakes Problem
> *"Namaste judges. In rural India, when a pregnant mother walks into a village health sub-centre with a blood pressure of 165/100 and severe headaches, seconds matter. This is severe pre-eclampsia—a leading cause of maternal mortality.*
>
> *Today, developers are building AI agents to assist in healthcare. But here is the fatal flaw: **giving autonomous LLMs direct access to call external APIs is dangerous**. LLMs hallucinate parameters, leak credentials, fail on intermittent rural networks, and can trigger duplicate ambulance dispatches."*

### [0:30 - 1:10] The Solution: Swytchcode as the Governed Execution Runtime
> *"To solve this, Aarogya Sahayak integrates **Swytchcode** as our enterprise AI tool execution and governance layer.*
>
> *Our AI agent never holds API keys and never makes raw HTTP calls. Instead, every action—from **Sarvam AI Indic voice translation** to **emergency ASHA and ambulance notifications**—executes through Swytchcode.*
>
> *Swytchcode gives us four life-critical guarantees:*
> 1. * **Zero-Token Exposure**: No API secrets ever touch the AI prompt context.*
> 2. * **Guaranteed Idempotency**: Life-saving emergency alerts are dispatched exactly once, even if rural 3G drops mid-flight.*
> 3. * **Pre-Execution Clinical Schema Validation**: Every BP and SpO2 value is strictly verified before hitting the wire.*
> 4. * **Real-Time Auditability**: Every single AI action is visible and logged live in the Swytchcode dashboard."*

### [1:10 - 1:50] The Live Demonstration (The "Show Me" Moment)
> *(Perform Action on Screen)*
> *"Let me show you this live. On our Citizen Mobile app, I speak in Marathi: 'I am 8 months pregnant, my head is throbbing and vision is blurry.'*
>
> *1. Our voice intake routes through Sarvam AI under Swytchcode governance.*  
> *2. Our deterministic clinical engine flags pre-eclampsia danger signs.*  
> *3. The AI triggers the tool `dispatch_emergency_asha_alert`.*  
>
> *Now watch this: Let's switch tabs to our **Swytchcode Dashboard at app.swytchcode.com**.*
> *(Point to the screen)*  
> *Here is the execution request that just arrived in real-time. Notice the status `200 OK`, latency `138ms`, zero PII leakage, and the unique idempotency trace. The ASHA worker in the village has already received the dispatch."*

### [1:50 - 2:00] Closing
> *"By uniting Sarvam AI's Indic voice intelligence with Swytchcode's governed execution runtime, Aarogya Sahayak makes AI in healthcare safe, deterministic, and ready for 1.4 billion citizens. Thank you!"*

---

## 2. Step-by-Step Live Demo Checklist

1. **Before Pitching**:
   - Open Tab 1: Aarogya Sahayak Citizen Mobile (`http://localhost:5173` or production URL).
   - Open Tab 2: [Swytchcode Dashboard Overview](https://app.swytchcode.com/dashboard/overview) logged in as `princesher321@gmail.com`.
   - Open Tab 3: Healthcare Portal / Doctor Dashboard.

2. **Triggering the Demo Flow**:
   - Go to Tab 1 (Citizen Assistant).
   - Type or speak:  
     `"Pregnant 32 weeks, severe headache, blurred vision, BP 160/100"`
   - Observe the immediate alert response with nearest PHC directions.

3. **Showing the Proof on Swytchcode**:
   - Switch to Tab 2 (`app.swytchcode.com/dashboard/overview`).
   - Refresh or show the live event stream:
     - Tool: `dispatch_emergency_asha_alert`
     - Response: `200 OK`
     - Status: `SUCCESS (IDEMPOTENT)`
   - Show the judges: *"See how Swytchcode recorded the latency and validated the clinical schema."*

---

## 3. Judge Q&A Cheat Sheet (Bulletproof Answers)

#### Q1: *"Why couldn't you just use Python's `requests` library or `fetch` with a `try/catch`?"*
> **Answer**:  
> *"In a simple prototype, you could. But in mission-critical healthcare, raw `requests` fails on three counts:*  
> *1. **Idempotency**: If a rural cell tower drops while sending an emergency notification, a basic retry will dispatch multiple ambulances. Swytchcode handles request deduplication via idempotency keys at the runtime layer.*  
> *2. **Prompt Injection & Credential Safety**: If an LLM decides when to call an API, exposing API keys in memory or giving the LLM code execution privileges creates severe security vulnerabilities. Swytchcode enforces an isolated execution boundary.*  
> *3. **Observability**: Swytchcode gives health administrators and compliance regulators a centralized audit trail of all AI tool executions without building bespoke logging microservices."*

#### Q2: *"What happens if Swytchcode or the internet is completely down in a remote village?"*
> **Answer**:  
> *"Aarogya Sahayak is architected with a **Deterministic Local Fallback Invariant**. If external cloud connectivity fails, our local adapter immediately falls back to on-device emergency SMS protocols and cached clinical guidance. The system will never freeze or fail silently."*

#### Q3: *"How does Sarvam AI fit into this?"*
> **Answer**:  
> *"Sarvam AI is the leading Indic voice foundation model (Saaras for speech recognition and Bulbul for natural speech synthesis). We routed Sarvam calls through Swytchcode's execution proxy so that voice latency budgets, audio chunk retries, and language policy constraints are uniformly governed."*
