from abc import ABCMeta, abstractmethod
from typing import Iterable


class State(metaclass=ABCMeta):

    def __init__(self, obj: object):
        pass

    @property
    @abstractmethod
    def value(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def end(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def legal_actions(self) -> Iterable['State']:
        raise NotImplementedError

    @abstractmethod
    def next(self) -> 'State':
        raise NotImplementedError

    @abstractmethod
    def playout(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def switched(self) -> bool:
        raise NotImplementedError

