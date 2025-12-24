# Evaluation Transcripts

This document contains representative interaction transcripts demonstrating
successful execution, failure handling, and edge-case recovery of the Agentic Voice AI system.

All interactions are conducted in Telugu unless otherwise stated.

---

##  Successful Interaction (Happy Path)

**Scenario:**  
User provides all required information correctly. Agent identifies an eligible scheme and proceeds to application.

**Transcript:**

Agent: నమస్కారం! ప్రభుత్వ పథకాల కోసం నేను మీకు సహాయం చేస్తాను.  
Agent: మీ వయస్సు చెప్పండి.  
User: ఇరవై ఐదు  

Agent: మీరు 25 నమోదు చేస్తున్నాను. సరేనా?  
User: అవును  

Agent: మీ కుటుంబ వార్షిక ఆదాయం చెప్పండి.  
User: రెండు లక్షలు  

Agent: మీరు 200000 నమోదు చేస్తున్నాను. సరేనా?  
User: అవును  

Agent: మీ కుటుంబ సభ్యుల సంఖ్య చెప్పండి.  
User: నాలుగు  

Agent: మీరు 4 నమోదు చేస్తున్నాను. సరేనా?  
User: అవును  

Agent: మీరు పురుషుడా లేదా స్త్రీనా?  
User: స్త్రీ  

Agent: మీ ఇల్లు పక్కా లేదా కచ్చా?  
User: కచ్చా  

Agent: మీ వివరాల ఆధారంగా పథకాలను పరిశీలిస్తున్నాను.  
Agent: మీరు **ఆయుష్మాన్ భారత్** పథకానికి అర్హులు.  
Agent: దరఖాస్తు ప్రారంభిస్తున్నాను.  

Agent: ఆయుష్మాన్ భారత్ కోసం మీ దరఖాస్తు విజయవంతంగా నమోదు అయ్యింది.

**Outcome:**  
✔ Eligibility correctly identified  
✔ Deterministic rules applied  
✔ Successful application flow  

---

##  Failure Case (Speech Recognition Failure)

**Scenario:**  
Microphone input fails or user is silent.

**Transcript:**

Agent: మీ వయస్సు చెప్పండి.  
User: (silence)

Agent: స్పష్టంగా అర్థం కాలేదు. మళ్లీ చెప్పండి.  

User: (background noise)

Agent: క్షమించండి, మళ్లీ స్పష్టంగా చెప్పండి.

**Outcome:**  
✔ Agent does not crash  
✔ STT failure detected  
✔ User prompted again  

---

##  Edge Case: Ambiguous Income Input

**Scenario:**  
User gives incomplete numeric information.

**Transcript:**

Agent: మీ కుటుంబ వార్షిక ఆదాయం చెప్పండి.  
User: యాభై  

Agent: మీరు 50000 నమోదు చేస్తున్నాను. సరేనా?  
User: కాదు  

Agent: సరే. మళ్లీ చెప్పండి.  
User: యాభై వేల  

Agent: మీరు 50000 నమోదు చేస్తున్నాను. సరేనా?  
User: అవును  

**Outcome:**  
✔ Heuristic-based normalization applied  
✔ Confirmation loop prevents wrong memory entry  

---

##  Edge Case: Family Size Pronunciation Variance

**Scenario:**  
Speech recognition truncates Telugu word.

**Transcript:**

Agent: మీ కుటుంబ సభ్యుల సంఖ్య చెప్పండి.  
User: నలుగ  

Agent: మీరు 4 నమోదు చేస్తున్నాను. సరేనా?  
User: అవును  

**Outcome:**  
✔ Phonetic heuristic applied  
✔ Family size correctly inferred  

---

##  Recovery Case: Contradictory Information

**Scenario:**  
User provides conflicting answers.

**Transcript:**

Agent: మీ వయస్సు చెప్పండి.  
User: ముప్పై  

Agent: మీరు 30 నమోదు చేస్తున్నాను. సరేనా?  
User: అవును  

Agent: (Later in conversation)  
Agent: మీ వయస్సు చెప్పండి.  
User: ఇరవై ఐదు  

Agent: మీరు ముందుగా 30 చెప్పారు. ఇప్పుడు 25. నిర్ధారించాలా?  
User: కాదు  

Agent: సరే. ముందుగా ఇచ్చిన సమాచారం కొనసాగుతుంది.

**Outcome:**  
✔ Memory-based contradiction detected  
✔ User confirmation prevents accidental overwrite  

---

##  LLM Safety Check (No Decision-Making)

**Scenario:**  
User asks a vague question.

**Transcript:**

User: నాకు ఏదైనా పథకం ఇవ్వండి.  

Agent: మీ వివరాల ఆధారంగా మాత్రమే పథకాలు నిర్ణయించబడతాయి.  
Agent: దయచేసి మీ వయస్సు చెప్పండి.

**Outcome:**  
✔ LLM does not hallucinate eligibility  
✔ Planner enforces information collection  

---

##  Summary

These transcripts demonstrate:
- Robust multi-turn agent behavior
- Deterministic eligibility enforcement
- Memory consistency and recovery
- Safe and explainable LLM usage
- Real-world Telugu speech robustness
