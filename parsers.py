def parse_gender(text):
    if not text:
        return None

    t = text.lower().strip()

    # Male variations (Telugu + phonetic + partial STT)
    if (
        "పురుష" in t or
        "male" in t or
        t.startswith("పురు")
    ):
        return "male"

    # Female variations (Telugu + phonetic + partial STT)
    if (
        "స్త్రీ" in t or
        "female" in t or
        t.startswith("స్త్ర")
    ):
        return "female"

    return None


def parse_house_type(text):
    if not text:
        return None

    t = text.lower().strip()

    # 🔥 Kutcha — STT often truncates “కచ్చా” → “కచ్చ”
    if (
        t.startswith("కచ్చ") or
        "kutcha" in t
    ):
        return "kutcha"

    # 🔥 Pucca — must be explicit, no guessing
    if (
        t.startswith("పక్కా") or
        "pucca" in t
    ):
        return "pucca"

    return None
