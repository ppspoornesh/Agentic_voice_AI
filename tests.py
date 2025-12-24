from unittest.mock import patch
from agent import run_agent

@patch("agent.get_voice_input")
@patch("agent.speak_text")
def test_agent(mock_speak, mock_input):
    mock_input.side_effect = [
        "ప్రభుత్వ పథకం",
        "నా వయస్సు ముప్పై",
        "ఆదాయం యాభై వేల",
        "కుటుంబ సభ్యులు నాలుగు"
    ]
    run_agent()
    print("Test passed")
