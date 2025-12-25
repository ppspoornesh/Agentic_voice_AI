from unittest.mock import patch
from agent import run_agent


@patch("agent.get_voice_input")
@patch("agent.speak_text")
def test_agent(mock_speak, mock_input):
    """
    Basic test to simulate a voice-based conversation.
    Voice input and output are mocked so the agent
    can be tested without a microphone or speaker.
    """

    # Simulated user voice responses in sequence
    mock_input.side_effect = [
        "ప్రభుత్వ పథకం",
        "నా వయస్సు ముప్పై",
        "ఆదాయం యాభై వేల",
        "కుటుంబ సభ్యులు నాలుగు"
    ]

    # Run the agent with mocked voice I/O
    run_agent()

    # If execution completes without error, test is considered successful
    print("Test passed")
