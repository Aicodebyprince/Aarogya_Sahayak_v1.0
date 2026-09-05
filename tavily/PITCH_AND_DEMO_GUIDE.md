# Pitch & Technical Judge Q&A Guide: Tavily AI

This guide contains the **2-Minute Elevator Pitch**, **Live Demo Flow**, and **Technical Judge Q&A Defense** for presenting the Tavily AI integration in **Aarogya Sahayak**.

---

## 1. The 2-Minute Judge Pitch Script

> *"Good morning, judges! In rural Indian healthcare, generative AI faces a deadly pitfall: **hallucinations in government welfare schemes**.*
>
> *When an ASHA health worker or a rural mother asks about maternity grants or hospital subsidies under Ayushman Bharat or PMMVY, traditional LLMs hallucinate dead links, quote obsolete guidelines, or worse—point users to fraudulent private portals.*
>
> *To solve this, we built a **Governed Real-Time Official Verification Engine** powered by **Tavily AI**.*
>
> *Here is how it works:*
> *First, we enforce a strict **Zero-Trust Indian Government Allowlist** using Tavily's native `include_domains` parameter. Every query is confined strictly to `.gov.in` and `.nic.in` domains—like `mohfw.gov.in`, `nha.gov.in`, and `pmjay.gov.in`.*
>
> *Second, we integrated an interactive **Live Verification Action** directly into our ASHA Healthcare Portal. With one click on any evaluated scheme, Tavily executes a live search, confirms the latest circular, and provides the authentic document link right on the screen.*
>
> *Third, our runtime security guard actively blocks any non-governmental link before it can ever reach a patient.*
>
> *By grounding our Multi-Agent clinical system with Tavily, we brought URL hallucinations down to **absolute zero** and gave rural frontline workers 100% verified confidence in life-saving public schemes."*

---

## 2. Live Technical Demo Flow (1 Minute)

1. **Step 1: Open Portal**: Navigate to `/asha/schemes`.
2. **Step 2: Show Scheme Card**: Scroll to **Pradhan Mantri Matru Vandana Yojana (PMMVY)**.
3. **Step 3: Trigger Tavily**: Click **`⚡ Live Verify via Tavily AI`**.
4. **Step 4: Show Verified Badge**: Point to the resulting **`🟢 Verified (pmssy.mohfw.gov.in)`** badge and the verified document link.
5. **Step 5: Run Terminal Negative Test**: Switch to terminal and run `python demo_tavily.py` to demonstrate Test 2 blocking an untrusted URL (`BLOCKED_NON_OFFICIAL_DOMAIN`).

---

## 3. Judge & Mentor Q&A Defense

### Q1: *"Why did you use Tavily instead of a standard Google Custom Search or SerpAPI?"*
> **Answer**:
> *"Tavily is purpose-built for LLM agents. Unlike traditional search APIs that return bloated HTML or ad-heavy snippets, Tavily returns clean, pre-parsed, structured markdown snippets designed specifically for agent consumption.  
> Crucially, Tavily's native `include_domains` parameter allows us to strictly enforce a whitelist of `.gov.in` and `.nic.in` at the engine level. This eliminates token bloat, reduces latency to ~2-4 seconds, and guarantees that no commercial blog spam is ever ingested into our clinical context."*

### Q2: *"What happens if Tavily is down or the village clinic has no internet?"*
> **Answer**:
> *"We implemented a 3-tier resilient fallback circuit. If Tavily is unreachable or the network drops, our service catches the exception and immediately falls back to a locally cached statutory guidelines dictionary derived from MoHFW and NHM master documents. The UI transparently indicates `MOCK_VERIFIED` or `OFFLINE_SNAPSHOT` so the healthcare worker is always aware of the data provenance."*

### Q3: *"Can a malicious prompt inject an unofficial search query to bypass your domain guard?"*
> **Answer**:
> *"No. The domain allowlist is enforced on two independent layers:  
> 1. At the Tavily API layer via `include_domains=['gov.in', 'nic.in', 'who.int']`.  
> 2. At our Python service layer using `is_domain_allowed()`, which parses the candidate URL's hostname using standard Python `urllib.parse` and rejects any hostname that does not match or end with an approved government domain. Even if an LLM attempted to pass a malicious URL, our security guard quarantines it with `BLOCKED_NON_OFFICIAL_DOMAIN`."*

### Q4: *"How does Tavily fit into your wider Multi-Agent architecture?"*
> **Answer**:
> *"Aarogya Sahayak uses a tri-factor retrieval pipeline:  
> 1. **Milvus Clinical RAG** provides static clinical protocols and emergency triage rules.  
> 2. **Neo4j Scheme Graph** provides deterministic, 3-valued eligibility checking across 29 national schemes based on patient demographics.  
> 3. **Tavily AI** serves as our external ground truth anchor, fetching dynamic operational updates, hospital empanelments, and live application URLs. Each engine has a clear boundary, eliminating hallucination at every step."*
