from abc import ABCMeta, abstractmethod
from typing import NoReturn

from games.cards.card import Card


class CardHolder(metaclass=ABCMeta):
    @abstractmethod
    def append(self, card) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def pop(self, name: str) -> Card:
        raise NotImplementedError
