import json

def load_schemes():
    with open("schemes.json", encoding="utf-8") as f:
        return json.load(f)


def retrieve_schemes(query=None):
    # For now, return all schemes.
    # Eligibility filtering is handled later deterministically.
    return load_schemes()


def check_eligibility(scheme, user):
    """
    Human-style eligibility explanation.
    Deterministic + explainable.
    """

    rules = scheme.get("rules", {})
    reasons = []

    # ---------- RULE CHECKS ----------
    if "gender" in rules:
        if user.get("gender") != rules["gender"]:
            return (
                f"మీరు ఇచ్చిన వివరాల ప్రకారం, "
                f"మీరు **{scheme['name']}**కు ప్రస్తుతం అర్హులు కాదు.\n"
                f"ఈ పథకం { 'మహిళలకు మాత్రమే' if rules['gender']=='female' else 'పురుషులకు మాత్రమే' } వర్తిస్తుంది.\n"
                f"ఇతర పథకాలను పరిశీలిస్తున్నాను."
            )

        reasons.append("మీరు మహిళ కావడం")

    if "min_age" in rules:
        if user.get("age", 0) < rules["min_age"]:
            return (
                f"{scheme['name']} కోసం మీరు అర్హులు కాదు.\n"
                f"ఈ పథకానికి కనీస వయస్సు {rules['min_age']} సంవత్సరాలు అవసరం."
            )
        reasons.append(f"మీ వయస్సు {rules['min_age']} సంవత్సరాలకు పైగా ఉండడం")

    if "max_income" in rules:
        if user.get("income", 0) > rules["max_income"]:
            return (
                f"{scheme['name']} కోసం మీరు అర్హులు కాదు.\n"
                f"మీ కుటుంబ ఆదాయం ఈ పథకం అర్హతకు మించి ఉంది."
            )
        reasons.append("మీ కుటుంబ ఆదాయం అర్హత పరిధిలో ఉండడం")

    if "max_family_size" in rules:
        if user.get("family_size", 0) > rules["max_family_size"]:
            return (
                f"{scheme['name']} కోసం మీరు అర్హులు కాదు.\n"
                f"కుటుంబ సభ్యుల సంఖ్య అర్హతకు మించి ఉంది."
            )
        reasons.append("మీ కుటుంబ సభ్యుల సంఖ్య అర్హతలో ఉండడం")

    # ---------- ELIGIBLE (HUMAN EXPLANATION) ----------
    reason_text = " మరియు ".join(reasons)

    return (
        f"మీరు ఇచ్చిన వివరాల ఆధారంగా,\n"
        f"మీరు **{scheme['name']}**కు అర్హులు.\n\n"
        f"కారణం ఏమిటంటే,\n"
        f"{reason_text}.\n\n"
        f"ఈ పథకం ద్వారా,\n"
        f"{scheme['description']}\n\n"
        f"ఇప్పుడు, మీ కోసం\n"
        f"ఈ పథకానికి సంబంధించిన దరఖాస్తు ప్రక్రియను ప్రారంభిస్తున్నాను."
    )


def mock_apply(scheme, user):
    return (
        f"{scheme['name']} కోసం మీ దరఖాస్తు విజయవంతంగా నమోదు అయ్యింది.\n"
        f"అధికారిక వెబ్‌సైట్: {scheme['application_link']}"
    )
