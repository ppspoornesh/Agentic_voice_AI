from enum import Enum

class AgentState(Enum):
    IDLE = 0
    PLANNING = 1
    COLLECTING_INFO = 2
    RETRIEVING = 3
    EVALUATING = 4
    APPLYING = 5
    RECOVERING = 6
    ERROR = 7
