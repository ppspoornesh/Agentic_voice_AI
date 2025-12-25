from enum import Enum

class AgentState(Enum):
    """
    Represents different stages of the agent's execution.
    This enum helps in understanding and tracking what the agent
    is currently doing during the conversation flow.
    """

    # Initial state before starting any interaction
    IDLE = 0

    # Agent is deciding what action to take next
    PLANNING = 1

    # Agent is collecting required information from the user
    COLLECTING_INFO = 2

    # Agent is retrieving available government schemes
    RETRIEVING = 3

    # Agent is checking eligibility based on user details
    EVALUATING = 4

    # Agent is performing the application step (mock apply)
    APPLYING = 5

    # Agent is handling errors like speech failure or wrong input
    RECOVERING = 6

    # Agent has encountered an unrecoverable error
    ERROR = 7
