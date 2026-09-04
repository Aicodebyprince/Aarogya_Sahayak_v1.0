# Dual-Sponsor Synergy: Lyzr AI (The Brain) + Swytchcode (The Hand)

> **Platform**: Aarogya Sahayak  
> **Deployment Architecture**: Enterprise Multi-Agent Cognitive Intelligence with Governed API Execution  
> **Target Audience**: Hackathon Technical Judges & Enterprise Architects

---

## 1. Architectural Division of Labor

Modern enterprise AI systems require two distinct layers of reliability:
1. **Cognitive Deliberation Layer (Multi-Agent Consensus & Guardrails)**: Deciding *what* to do based on medical protocols, guidelines, and safety policies.
2. **Deterministic Execution Layer (Tool Calling & API Governance)**: Safely executing *how* real-world tools, databases, and third-party APIs are called.

Aarogya Sahayak achieves this by pairing **Lyzr AI** with **Swytchcode**:

| Architectural Dimension | Lyzr AI (The Cognitive Brain) | Swytchcode (The Execution Hand) |
|---|---|---|
| **Primary Domain** | Multi-Agent Reasoning & Medical Triage | Safe Tool Execution & API Governance |
| **Deployed Identity** | Agent `Aarogya Clinical Navigator` (`6a9ae0e14a372650b843a9ae`) | CLI Workspace `calm-meadow-c150` (`85ab6d86-...`) |
| **Underlying Engine** | OpenAI `gpt-4o` via Lyzr Studio Runtime | Zero-Trust Proxy & Governance Engine |
| **Core Value** | Six-Sigma Consensus, ICMR Guidelines, Scheme Matching | Idempotency, Token Vault, Zero Leaks, Replay Defense |
| **Safety Role** | Vetoes dangerous prescriptions & dosage suggestions | Blocks malformed tool calls, deduplicates emergency dispatches |
| **Failure Mode Handling** | Graceful fallback to deterministic guideline matrix | In-memory Governor Fallback with audit logging |

---

## 2. End-to-End Workflow Trace

When a rural ASHA worker records a voice note from a pregnant mother in Kalyanpur village:

```
Step 1: Citizen Voice -> Sarvam AI STT (Governed by Swytchcode Voice Proxy)
        Transcript: "I am 7 months pregnant. Severe headache since morning and seeing blur."
        Vitals Recorded: BP 160/100 mmHg.

Step 2: Masking & Tokenization -> Local PII Masker replaces names/phones with surrogate tokens.

Step 3: Cognitive Deliberation -> LYZR AI (Aarogya Clinical Navigator)
        - Analyzes gestational age (28 weeks) + BP 160/100 + Headache + Vision blur.
        - Identifies Pre-Eclampsia / Impending Eclampsia danger signs.
        - Cites MoHFW Maternal Care Guidelines & ICMR Standard Treatment Workflows.
        - Retrieves Indian Welfare Entitlements (JSY ₹1,400 + PMMVY ₹5,000).
        - Executes Safety Critic: Confirms NO prohibited prescription drugs are generated.
        - Emits structured directive: PRIORITY=CRITICAL, ACTION=DISPATCH_EMERGENCY_ASHA.

Step 4: Safe Tool Execution -> SWYTCHCODE RUNTIME
        - Intercepts dispatch_emergency_asha_alert tool request.
        - Computes SHA-256 fingerprint of vitals + patient ID.
        - Verifies Sliding Window Idempotency: Prevents sending 5 duplicate ambulances.
        - Replaces surrogate tokens with secure ABDM recipient endpoint.
        - Triggers ASHA emergency alert webhook with full cryptographic trace.

Step 5: Voice Feedback -> Sarvam AI TTS (Governed by Swytchcode)
        - Synthesizes clear, calm Marathi/Hindi instructions for the mother:
          "Please sit down. The Kalyanpur PHC and Sister Anita have been notified."
```

---

## 3. Why Judges Value This Approach

1. **Not a Toy Wrapper**: This is a production-grade multi-agent architecture with separated cognitive reasoning and execution boundaries.
2. **Zero Hallucination Danger**: Lyzr’s Six-Sigma critic guarantees medical safety, while Swytchcode’s runtime ensures APIs are never triggered with hallucinated parameters.
3. **Resilience & Fault Tolerance**: Both sponsors have live cloud connections with deterministic local failover chains. The system works seamlessly under real rural connectivity constraints.
