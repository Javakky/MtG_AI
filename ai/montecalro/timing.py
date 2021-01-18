from enum import Enum, auto


class Timing(Enum):
    AFTER_START = auto()
    SELECT_ATTACKER = auto()
    SELECT_BLOCKER = auto()
    PLAY_LAND = auto()
    PLAY_SPELL = auto()


def next(now: 'Timing') -> 'Timing':
    if now == Timing.AFTER_START:
        return Timing.SELECT_ATTACKER
    if now == Timing.SELECT_ATTACKER:
        return Timing.SELECT_BLOCKER
    if now == Timing.SELECT_BLOCKER:
        return Timing.PLAY_LAND
    if now == Timing.PLAY_LAND:
        return Timing.PLAY_SPELL
    if now == Timing.PLAY_SPELL:
        return Timing.SELECT_ATTACKER
