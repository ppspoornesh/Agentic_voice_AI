import os, time, re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def enforce_telugu(text):
    if not text:
        return "దయచేసి మళ్లీ ప్రయత్నించండి."
    ratio = len(re.findall(r"[a-zA-Z]", text)) / max(len(text), 1)
    if ratio > 0.25:
        return "దయచేసి తెలుగులో మాత్రమే సమాధానం ఇవ్వండి."
    return text.strip()

def call_llm(prompt, retries=2):
    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "మీరు ప్రభుత్వ పథకాలపై సహాయం చేసే తెలుగులో మాత్రమే మాట్లాడే సహాయకుడు."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        text = res.choices[0].message.content
        text = text.replace("```json", "").replace("```", "")
        return enforce_telugu(text)
    except Exception:
        if retries <= 0:
            return "సేవ ప్రస్తుతం అందుబాటులో లేదు."
        time.sleep(1)
        return call_llm(prompt, retries - 1)
