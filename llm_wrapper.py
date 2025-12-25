import os
import time
import re
from groq import Groq

# Initialize Groq client using API key from environment variables
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def enforce_telugu(text):
    """
    Ensures the response is mostly in Telugu.
    If too much English is detected, a Telugu-only message is returned.
    This helps keep the conversation consistent for end users.
    """
    if not text:
        return "దయచేసి మళ్లీ ప్రయత్నించండి."

    # Calculate how much of the text is English
    ratio = len(re.findall(r"[a-zA-Z]", text)) / max(len(text), 1)

    if ratio > 0.25:
        return "దయచేసి తెలుగులో మాత్రమే సమాధానం ఇవ్వండి."

    return text.strip()


def call_llm(prompt, retries=2):
    """
    Sends a prompt to the LLM and returns a Telugu response.
    Includes basic retry logic to handle temporary API failures.
    """
    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "మీరు ప్రభుత్వ పథకాలపై సహాయం చేసే తెలుగులో మాత్రమే మాట్లాడే సహాయకుడు."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        # Extract and clean the model output
        text = res.choices[0].message.content
        text = text.replace("```json", "").replace("```", "")

        return enforce_telugu(text)

    except Exception:
        # Retry in case of network or service issues
        if retries <= 0:
            return "సేవ ప్రస్తుతం అందుబాటులో లేదు."

        time.sleep(1)
        return call_llm(prompt, retries - 1)
