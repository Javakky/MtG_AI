from enum import Enum, auto


class Timing(Enum):
    AFTER_START = auto()
    SELECT_ATTACKER = auto()
    SELECT_BLOCKER = auto()
    PLAY_LAND = auto()
    PLAY_SPELL = auto()
