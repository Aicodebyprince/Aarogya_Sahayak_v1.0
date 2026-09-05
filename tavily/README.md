# Tavily × Aarogya Sahayak: Governed Real-Time Official Verification

> **Hackathon Track**: AI Agent Search, Real-Time Information Retrieval & Safety Governance  
> **Project**: Aarogya Sahayak (AI-Powered Voice-First Rural Healthcare Platform for India)  
> **Sponsor Platform**: [Tavily AI (tavily.com)](https://tavily.com/)  
> **Deployment**: Production & Staging (Render Singapore + Vercel)  
> **Live API Status**: `CONNECTED` (`LIVE_VERIFIED`)

---

## Executive Summary

In public healthcare delivery and social welfare programs across India, false or outdated information can have devastating consequences. When a pregnant woman in a remote village asks an AI assistant about hospital subsidies or when an ASHA worker checks current antenatal care guidelines, relying on static LLM knowledge creates dangerous risks: **stale rules, hallucinated 404 links, and zero protection against phishing scams**.

By integrating **Tavily AI**, Aarogya Sahayak implements a **Governed Real-Time Official Web Verification Engine** with a strict **Zero-Trust Indian Government Allowlist (`.gov.in`, `.nic.in`)**.

Tavily acts as the external truth anchor in our multi-agent architecture:
1. **Validating Policy Updates**: Retrieves real-time circulars from the Ministry of Health and Family Welfare (MoHFW) and Ministry of Women & Child Development (MoWCD).
2. **Eliminating Phishing Links**: Uses Tavily's native `include_domains` parameter to physically restrict all searches to verified government domains.
3. **Audit Trail Provenance**: Supplies health workers and judges with verified document titles, canonical government URLs, and timestamps.

---

## Key Value Pillars

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   TAVILY REAL-TIME VERIFICATION ENGINE LAYER                     │
├───────────────────────┬─────────────────────────┬────────────────────────────────┤
│   ZERO-TRUST DOMAIN   │   REAL-TIME POLICY      │    100% VALID GOVERNMENT URLS  │
│      ALLOWLIST        │       FRESHNESS         │                                │
│  Exclusively queries  │  Fetches post-cutoff    │  Eliminates link hallucinations│
│  .gov.in, .nic.in,    │  circulars, grants, and │  and protects rural citizens   │
│  and statutory bodies.│  revised benefit norms. │  from cyber-phishing traps.    │
├───────────────────────┼─────────────────────────┼────────────────────────────────┤
│  PROVENANCE & AUDIT   │  ONE-CLICK PORTAL UI    │    RESILIENT FALLBACK          │
│       METADATA        │       BADGE             │         CIRCUIT                │
│  Every claim links to │  ASHA workers verify    │  If network drops, gracefully  │
│  authentic title, URL,│  guidelines on screen   │  falls back to verified local  │
│  domain, and latency. │  with a single click.   │  statutory database snapshots. │
└───────────────────────┴─────────────────────────┴────────────────────────────────┘
```

---

## Directory Index

This directory contains the complete Tavily integration suite, technical blueprints, and video shooting assets:

| File | Description |
|---|---|
| [AarogyaSahayak_Tavily_Architecture_and_Proof.pdf](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/tavily/AarogyaSahayak_Tavily_Architecture_and_Proof.pdf) | **Publication-Grade PDF Whitepaper**: 2-page executive architectural specification, Before vs After matrix, clinical case study, and live proof. |
| [AarogyaSahayak_Tavily_Architecture_and_Proof.docx](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/tavily/AarogyaSahayak_Tavily_Architecture_and_Proof.docx) | **Editable Word Whitepaper**: Formatted DOCX version for submission portals and grant reviewers. |
| [BEFORE_VS_AFTER.md](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/tavily/BEFORE_VS_AFTER.md) | Exhaustive breakdown: How we handled scheme data before Tavily vs. how Tavily solves it with real-world case studies. |
| [INTEGRATION_ARCHITECTURE.md](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/tavily/INTEGRATION_ARCHITECTURE.md) | Deep technical architecture detailing the Multi-Agent tri-factor (Milvus RAG + Neo4j Graph + Tavily Search). |
| [LIVE_VERIFICATION_AND_DEMO_GUIDE.md](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/tavily/LIVE_VERIFICATION_AND_DEMO_GUIDE.md) | Step-by-step video shooting script, recording walkthrough, terminal commands, and talking points. |
| [TAVILY_INTEGRATION_SHOWCASE.html](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/tavily/TAVILY_INTEGRATION_SHOWCASE.html) | Interactive HTML showcase demonstrating live tests, domain guards, and before/after comparisons. |
| [tavily_manifest.json](file:///c:/Users/princ/Downloads/AarogyaSahayak-main/AarogyaSahayak-main/tavily/tavily_manifest.json) | Production integration manifest containing approved domain lists, endpoints, and governance settings. |

---

## The 3 Core Capabilities Powered by Tavily

### 1. Live Welfare Scheme Verification (`verify_official_update`)
* **Trigger**: A citizen or ASHA worker queries benefits for schemes like PMMVY, PM-JAY, or Janani Suraksha Yojana.
* **Function**: Executes a search targeted specifically at `.gov.in` and `.nic.in` domains, pulling latest operational circulars.
* **Guarantee**: Never presents an unofficial commercial blog as authoritative advice.

### 2. Zero-Trust Domain Allowlist Guard
* **Trigger**: Any candidate link is evaluated prior to delivery to field staff or citizens.
* **Function**: Inspects hostname against strict allowlist (`mohfw.gov.in`, `nha.gov.in`, `pmjay.gov.in`, `abdm.gov.in`, `icmr.gov.in`, `nhm.gov.in`, `jeevandayee.gov.in`, `who.int`).
* **Guarantee**: Non-governmental URLs are immediately flagged as `BLOCKED_NON_OFFICIAL_DOMAIN`.

### 3. Integrated Healthcare Portal Verification UI
* **Location**: Healthcare Portal -> ASHA Schemes Screen (`/asha/schemes`).
* **Function**: Real-time **"⚡ Live Verify via Tavily AI"** button on each evaluated scheme card.
* **Guarantee**: Instantly returns live verified government circular title, canonical link, and green badge.

---

## Quick Verification Commands

### 1. Run Live Tavily Demonstration Script
```powershell
cd backend
.venv\Scripts\python.exe demo_tavily.py
```

### 2. Test Live Tavily Integration via Pytest
```powershell
cd backend
.venv\Scripts\pytest -o pythonpath=. tests/test_integrations_deep.py tests/test_live_integrations.py
```

### 3. Query Real-Time API Endpoint via Curl
```powershell
curl -X POST "http://localhost:8000/api/ai/tavily/verify" ^
     -H "Content-Type: application/json" ^
     -d "{\"query\": \"Pradhan Mantri Matru Vandana Yojana\"}"
```
