import re


def normalize_stt_noise(text):
    """
    Normalizes common speech-to-text errors.
    Handles broken words, mixed English outputs,
    and common Telugu number variations.
    """
    if not text:
        return text

    replacements = {
        "lak sha lu": "lakshalu",
        "lak shalu": "lakshalu",
        "lakh": "lakshalu",
        "lakhs": "lakshalu",
        "లక్షలు": "లక్ష",
        "లక్ష": "లక్ష",
        "ల": "లక్ష",        # STT sometimes outputs partial syllables
        "వేల": "వెయ్యి"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text.lower().strip()


# Telugu number words and their numeric values
UNITS = {
    "సున్నా": 0,
    "ఒక": 1, "ఒకటి": 1, "ఒకరు": 1,
    "రెండు": 2, "ఇద్దరు": 2,
    "మూడు": 3, "ముగ్గురు": 3,
    "నాలుగు": 4, "నలుగురు": 4,
    "ఐదు": 5, "ఐదుగురు": 5,
    "ఆరు": 6, "ఆరుగురు": 6,
    "ఏడు": 7, "ఏడుగురు": 7,
    "ఎనిమిది": 8, "ఎనిమిదుగురు": 8,
    "తొమ్మిది": 9, "తొమ్మిదుగురు": 9,

    # Common phonetic outputs from English-based STT
    "okati": 1,
    "rendu": 2, "iddaru": 2,
    "moodu": 3, "mugguru": 3,
    "nalugu": 4, "naluguru": 4,
    "aidu": 5, "aiduguru": 5
}

# Multipliers used in spoken numbers
MULTIPLIERS = {
    "వంద": 100,
    "వెయ్యి": 1000,
    "లక్ష": 100000,
    "lakshalu": 100000,
    "thousand": 1000,
    "hundred": 100
}


def extract_number(text):
    """
    Extracts a numeric value from Telugu speech input.
    Supports digits, word-based numbers, and common STT errors.
    """
    if not text:
        return None

    text = normalize_stt_noise(text)

    # If digits are present, directly use them
    digit = re.search(r"\d+", text)
    if digit:
        return int(digit.group())

    tokens = text.split()

    total = 0
    current = 0
    found = False

    # Parse tokens one by one to build the number
    for tok in tokens:
        tok = tok.strip()

        if tok in UNITS:
            current += UNITS[tok]
            found = True

        elif tok in MULTIPLIERS:
            # Handle cases like "లక్ష" without explicit "one"
            if current == 0:
                current = 1
            current *= MULTIPLIERS[tok]
            total += current
            current = 0
            found = True

    total += current

    # Fallback check for partial word matches
    if not found:
        for k, v in UNITS.items():
            if k in text:
                return v

    return total if found else None
