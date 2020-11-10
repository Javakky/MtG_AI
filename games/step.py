from enum import Enum, auto


class Step(Enum):
    UNTAP_STEP = auto()
    UPKEEP_STEP = auto()
    DRAW_STEP = auto()
    MAIN_PHASE = auto()
    DECLARE_ATTACKERS_STEP = auto()
    DECLARE_BLOCKERS_STEP = auto()
    COMBAT_DAMAGE_STEP = auto()
    END_STEP = auto()
