from enum import Enum, auto


class Timing(Enum):
    AFTER_START = auto()
    SELECT_ATTACKER = auto()
    SELECTED_ATTACKER = auto()
    SELECT_BLOCKER = auto()
    BEFORE_LAND = auto()
    PLAY_LAND = auto()
    PLAY_SPELL = auto()


def next(now: 'Timing') -> 'Timing':
    if now == Timing.AFTER_START or now == Timing.PLAY_SPELL:
        return Timing.SELECT_ATTACKER
    if now == Timing.SELECT_ATTACKER or now == Timing.SELECTED_ATTACKER:
        return Timing.SELECT_BLOCKER
    if now == Timing.SELECT_BLOCKER or now == Timing.BEFORE_LAND:
        return Timing.PLAY_LAND
    if now == Timing.PLAY_LAND:
        return Timing.PLAY_SPELL
