from abc import ABCMeta, abstractmethod

from game.card.CardType import CardType


class Card(metaclass=ABCMeta):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def type(self) -> CardType:
        raise NotImplementedError

    @abstractmethod
    def clone(self) -> 'Card':
        raise NotImplementedError
