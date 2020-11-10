from abc import ABCMeta, abstractmethod

from games.cards.card_type import CardType


class Card(metaclass=ABCMeta):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def has_type(self, card_type: CardType) -> bool:
        raise NotImplementedError

    @abstractmethod
    def type(self) -> CardType:
        raise NotImplementedError

    @abstractmethod
    def clone(self) -> 'Card':
        raise NotImplementedError
