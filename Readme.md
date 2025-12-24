# Telugu Voice Agent for Government Schemes

This repository contains an agentic, voice-first AI assistant that helps users identify and apply for eligible Indian government schemes using Telugu speech.

Repository: telugu_voice_agent_schemes

---

##  Overview
The system supports multi-turn voice interaction, deterministic eligibility checking, memory-based reasoning, and robust failure recovery.  
It is designed to handle real-world speech ambiguity in Telugu.

---

##  Key Features
- Telugu voice interaction (Speech-to-Text + Text-to-Speech)
- Agentic planning with explicit state transitions
- SQLite-based conversational memory
- Deterministic eligibility engine (no hallucinations)
- Domain-specific speech parsing and heuristics
- Hybrid Text-to-Speech with offline fallback
- Graceful recovery from STT and parsing failures

---

##  Architecture
**Core Components:**
- Speech-to-Text: Google STT
- Agent Core:
  - Planner (decision making)
  - Memory (SQLite)
  - Parsers & heuristics
- Eligibility Engine (rule-based)
- LLM (Groq / LLaMA): explanations only
- Text-to-Speech:
  1. gTTS (online)
  2. pyttsx3 (offline)
  3. Text fallback

See `docs/architecture.png` for the system diagram.

---

##  Setup Instructions

###  Clone Repository
```bash
git clone https://github.com/<your-username>/telugu_voice_agent_schemes.git
cd telugu_voice_agent_schemes

