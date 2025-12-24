REQUIRED_FIELDS = [
    "age",
    "income",
    "family_size",
    "gender",
    "house_type"
]

def plan_next_action(memory, last_error=None, last_key=None):
    if last_error in ["STT_ERROR", "PARSE_ERROR"]:
        return "COLLECT", last_key

    for field in REQUIRED_FIELDS:
        if field not in memory:
            return "COLLECT", field

    return "SEARCH", "ready"
