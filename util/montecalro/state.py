from abc import ABCMeta
from typing import Iterable


class State(metaclass=ABCMeta):

    def __init__(self, obj: object):
        pass

    @property
    def value(self) -> float:
        raise NotImplementedError

    @property
    def end(self) -> bool:
        raise NotImplementedError

    @property
    def legal_actions(self) -> Iterable:
        raise NotImplementedError

    def next(self, obj: object) -> 'State':
        raise NotImplementedError

    def playout(self) -> float:
        raise NotImplementedError
