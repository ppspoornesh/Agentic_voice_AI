# List of mandatory fields required to evaluate scheme eligibility
REQUIRED_FIELDS = [
    "age",
    "income",
    "family_size",
    "gender",
    "house_type"
]


def plan_next_action(memory, last_error=None, last_key=None):
    """
    Decides what the agent should do next based on:
    - Information already collected
    - Any previous error
    - The last field that failed
    """

    # If there was a speech or parsing error, retry the same question
    if last_error in ["STT_ERROR", "PARSE_ERROR"]:
        return "COLLECT", last_key

    # Check which required detail is missing and ask for it
    for field in REQUIRED_FIELDS:
        if field not in memory:
            return "COLLECT", field

    # If all required details are available, move to scheme search
    return "SEARCH", "ready"
