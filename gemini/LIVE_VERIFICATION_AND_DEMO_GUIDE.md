# Google Gemini Live Verification & Hackathon Demo Guide

This guide provides end-to-end instructions for demonstrating **Aarogya Sahayak's Google Gemini Reasoning Engine** during hackathon judging, technical reviews, and mentor walkthroughs.

---

## 1. Quick Verification & Health Check

### Verify Service Status via API
Run this curl command against the running backend:

```bash
curl -X GET "http://localhost:8000/api/v1/ai/status" \
     -H "Accept: application/json"
```

**Expected JSON Response**:
```json
{
  "provider": "GEMINI",
  "configured": true,
  "reachable": true,
  "mode": "LIVE",
  "model": "gemini-2.5-flash",
  "last_error_category": null,
  "pii_masking_active": true
}
```

---

## 2. Live Demo Scenarios for Judges

### Scenario A: Colloquial Indic Symptom Triage (Marathi)
* **Context**: A pregnant rural mother expresses complications using everyday Marathi phrasing.
* **Citizen Input**:
  > *"ताई, मी सात महिन्यांची गरोदर आहे. सकाळपासून डोके खूप दुखतेय आणि डोळ्यांसमोर अंधारी येत आहे."*

* **Execute via cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/ai/citizen-turn" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "ताई, मी सात महिन्यांची गरोदर आहे. सकाळपासून डोके खूप दुखतेय आणि डोळ्यांसमोर अंधारी येत आहे.",
    "preferred_language": "mr-IN",
    "conversation_history": []
  }'
```

* **What to Highlight to Judges**:
  1. **Stage 1 Extraction**: Notice how Gemini extracts `gestational_age=7_months`, `symptoms=['headache', 'visual_disturbance']`, and classifies intent as `MATERNAL_COMPLICATION_TRIAGE`.
  2. **Stage 2 Generation**: The generated Marathi audio script is culturally empathetic, provides reassuring instructions, avoids illegal pharmaceutical prescriptions, and advises visiting the nearest PHC.
  3. **Triage Severity**: Urgency is automatically set to `RED_EMERGENCY`.

---

### Scenario B: Pediatric Triage & Dehydration Guard (Hindi)
* **Context**: A father reports a young child suffering from acute vomiting and diarrhea.
* **Citizen Input**:
  > *"मेरे ३ साल के बच्चे को कल रात से उल्टी और दस्त हैं और उसने सुबह से पेशाब भी नहीं किया।"*

* **Execute via cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/ai/citizen-turn" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "मेरे ३ साल के बच्चे को कल रात से उल्टी और दस्त हैं और उसने सुबह से पेशाब भी नहीं किया।",
    "preferred_language": "hi-IN",
    "conversation_history": []
  }'
```

* **What to Highlight to Judges**:
  1. **Clinical Acumen**: Gemini instantly identifies the absence of urination as a critical red flag for severe dehydration.
  2. **Clarifying Question**: It generates a high-priority clarifying question asking if the child is lethargic or able to drink fluids.
  3. **Immediate Home Care**: Recommends continuous administration of ORS (Oral Rehydration Solution) while preparing for clinic transfer.

---

### Scenario C: PII Masking & Privacy Audit
* **Context**: A citizen inadvertently types their private 12-digit Aadhaar number and phone number into the medical chat.
* **Citizen Input**:
  > *"मेरा नाम रमेश है, आधार नंबर 4582 9102 3841 और फोन 9823012345 है। मुझे सीने में तेज दर्द है।"*

* **What Happens Under the Hood**:
  1. `PIIMasker` intercepts the input.
  2. The prompt sent to Google Gemini reads:
     > *"मेरा नाम [PATIENT] है, आधार नंबर [AADHAAR_HASH_4f8a] और फोन [PHONE_MASKED] है। मुझे सीने में तेज दर्द है।"*
  3. **Judges' Takeaway**: Complete compliance with the Digital Personal Data Protection (DPDP) Act; third-party AI models never receive unencrypted citizen PII.

---

## 3. UI Live Demo Flow (PWA & ASHA Portal)

1. **Launch the Citizen PWA**: Navigate to `http://localhost:5173/chat`.
2. **Switch Language**: Select **Hindi (हिंदी)** or **Marathi (मराठी)** from the top-right selector.
3. **Trigger Voice Input**: Click the microphone icon and speak symptoms or type in colloquial terms.
4. **Observe Response Speed**: Gemini generates structured triage in under 1.5 seconds.
5. **Switch to ASHA Portal**: Navigate to `http://localhost:5173/asha/dashboard`. Notice how the emergency triage event automatically populated the high-risk alert queue for the assigned village health worker!

---

## 4. Anticipated Technical Q&A for Judges

**Q: Why use Google Gemini over generic OpenAI or open-source LLMs?**  
> *"Gemini provides state-of-the-art multilingual comprehension across Indian languages and scripts without translation lag. Its structured output mode adheres strictly to our Pydantic schema contracts, eliminating parser failures. Furthermore, Gemini's low latency and high context window allow us to pass multi-turn clinical guidelines and vector embeddings seamlessly."*

**Q: How do you prevent medical hallucination?**  
> *"We decouple understanding from response synthesis. Gemini Stage 1 only extracts structured clinical facts. Those facts are then cross-referenced against deterministic MoHFW/WHO clinical guideline thresholds (via Milvus RAG). Gemini Stage 2 is constrained to only synthesize natural, non-diagnostic audio scripts based on these verified facts. It is physically prohibited by prompt constraints and schema filters from prescribing medications."*

**Q: What happens if the internet goes down in a remote village?**  
> *"Our GeminiService implements `LIMITED_FALLBACK`. If the cloud API is unreachable or rate-limited, the system falls back to a deterministic, rule-based clinical triage engine running locally on the server. The citizen and ASHA worker never experience a broken UI or empty screen."*
