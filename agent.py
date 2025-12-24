import uuid
from voice_io import get_voice_input, speak_text
from telugu_numbers import extract_number
from memory import save_memory, memory_snapshot, check_contradiction
from planner import plan_next_action
from tools import retrieve_schemes, check_eligibility, mock_apply
from parsers import parse_gender, parse_house_type

QUESTIONS = {
    "age": "మీ వయస్సు చెప్పండి.",
    "income": "మీ కుటుంబ వార్షిక ఆదాయం చెప్పండి.",
    "family_size": "మీ కుటుంబ సభ్యుల సంఖ్య చెప్పండి.",
    "gender": "మీరు పురుషుడా లేదా స్త్రీనా?",
    "house_type": "మీ ఇల్లు పక్కా లేదా కచ్చా?"
}

CONFIRM_WORDS = [
    "అవును", "అవునండి",
    "సరే", "సరేండి",
    "ok", "okay", "yes",
    "sare", "sarey", "sari", "sare andi"
]

NEGATIVE_WORDS = [
    "కాదు", "కాదండి",
    "సరి కాదు", "సరే కాదు",
    "no", "nope", "cancel"
]

def is_confirmation(text):
    if not text:
        return False
    t = text.lower().strip()
    if any(n in t for n in NEGATIVE_WORDS):
        return False
    if any(p in t for p in CONFIRM_WORDS):
        return True
    return False


def log_state(tag, msg=""):
    print(f"[{tag}] {msg}")


def run_agent():
    session_id = str(uuid.uuid4())
    last_error = None
    last_key = None

    speak_text("నమస్కారం! ప్రభుత్వ పథకాల కోసం నేను మీకు సహాయం చేస్తాను.")

    while True:
        memory = memory_snapshot(session_id)
        action, key = plan_next_action(memory, last_error, last_key)

        # ================= COLLECT =================
        if action == "COLLECT":
            last_key = key
            log_state("COLLECTING", key)
            speak_text(QUESTIONS[key])
            speak_text("వింటున్నాను…")

            reply = get_voice_input()
            if not reply:
                log_state("ERROR", "STT failed")
                last_error = "STT_ERROR"
                continue

            log_state("RAW_INPUT", reply)

            # ---------- PARSING ----------
            if key in ["age", "income", "family_size"]:
                value = extract_number(reply)

                # 🔥 UPDATE-4: FAMILY SIZE NEVER FAILS
                if value is None and key == "family_size":
                    r = reply.lower().strip()

                    FAMILY_SIZE_SOUND_MAP = {
                        # Telugu
                        "ఒ": 1, "రె": 2, "మూ": 3, "న": 4,
                        "ఐ": 5, "ఆ": 6, "ఏ": 7, "ఎ": 8, "తొ": 9,

                        # Phonetic / English STT
                        "oka": 1, "one": 1,
                        "ren": 2, "two": 2,
                        "moo": 3, "three": 3,
                        "nal": 4, "four": 4,
                        "aid": 5, "five": 5,
                        "aar": 6, "six": 6,
                        "edu": 7, "seven": 7,
                        "eni": 8, "eight": 8,
                        "tho": 9, "nine": 9
                    }

                    for k, v in FAMILY_SIZE_SOUND_MAP.items():
                        if r.startswith(k):
                            value = v
                            log_state(
                                "HEURISTIC",
                                f"family_size inferred as {v} from sound '{k}'"
                            )
                            break

                if value is None:
                    log_state("ERROR", "Parse failed")
                    speak_text("స్పష్టంగా అర్థం కాలేదు. మళ్లీ చెప్పండి.")
                    last_error = "PARSE_ERROR"
                    continue

                # Income normalization (unchanged)
                if key == "income":
                    r = reply.lower()
                    if "లక్ష" in r or "laksh" in r:
                        value *= 100000
                    elif "వెయ్యి" in r or "thousand" in r:
                        value *= 1000
                    else:
                        value = value * 100000 if value < 20 else value * 1000

            elif key == "gender":
                value = parse_gender(reply)
                if not value:
                    speak_text("పురుషుడు లేదా స్త్రీ అని చెప్పండి.")
                    continue

            elif key == "house_type":
                value = parse_house_type(reply)
                if not value:
                    speak_text("పక్కా లేదా కచ్చా అని స్పష్టంగా చెప్పండి.")
                    continue

            log_state("PARSED", f"{key}={value}")

            # ---------- CONFIRM ----------
            speak_text(f"{value} నమోదు చేస్తున్నాను. సరేనా?")
            confirm = get_voice_input()

            if not is_confirmation(confirm):
                log_state("REJECTED", key)
                speak_text("సరే. మళ్లీ చెప్పండి.")
                continue

            contradiction = check_contradiction(session_id, key, value)
            if contradiction:
                speak_text(contradiction)
                if not is_confirmation(get_voice_input()):
                    continue

            save_memory(session_id, key, value)
            log_state("SAVED", key)
            last_error = None
            continue

        # ================= SEARCH =================
        if action == "SEARCH":
            speak_text("మీ వివరాల ఆధారంగా పథకాలను పరిశీలిస్తున్నాను.")
            schemes = retrieve_schemes(None)

            for scheme in schemes:
                log_state("EVALUATING", scheme["name"])
                explanation = check_eligibility(scheme, memory)
                speak_text(explanation)

                if "అర్హులు." in explanation:
                    speak_text("దరఖాస్తు ప్రారంభిస్తున్నాను.")
                    speak_text(mock_apply(scheme, memory))
                    return

            speak_text("ఈ వివరాలతో సరిపోయే పథకం లేదు.")
            return


if __name__ == "__main__":
    run_agent()
