def parse_gender(text):
    """
    Parses gender from user speech input.
    Handles Telugu words, English words, and partial STT outputs.
    """
    if not text:
        return None

    t = text.lower().strip()

    # Male keywords and common STT variations
    if (
        "పురుష" in t or
        "male" in t or
        t.startswith("పురు")
    ):
        return "male"

    # Female keywords and common STT variations
    if (
        "స్త్రీ" in t or
        "female" in t or
        t.startswith("స్త్ర")
    ):
        return "female"

    return None


def parse_house_type(text):
    """
    Identifies whether the house type is pucca or kutcha.
    Includes handling for truncated or partial STT outputs.
    """
    if not text:
        return None

    t = text.lower().strip()

    # Kutcha house detection (STT may cut the last vowel)
    if (
        t.startswith("కచ్చ") or
        "kutcha" in t
    ):
        return "kutcha"

    # Pucca house detection (kept strict to avoid wrong assumptions)
    if (
        t.startswith("పక్కా") or
        "pucca" in t
    ):
        return "pucca"

    return None
