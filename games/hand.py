from typing import List, Type, TypeVar

from games.cards.card import Card
from util.util import assert_instanceof


class Hand:
    C = TypeVar('C', bound=Card)

    def __init__(self):
        self.cards: List[Card] = []

    def append(self, card: Card):
        self.cards.append(card)

    def pop(self, index: int, type: Type[C] = Card) -> C:
        assert_instanceof(self.cards[index], type)
        return self.cards.pop(index)

    def get(self, index: int, type: Type[C] = Card) -> C:
        assert_instanceof(self.cards[index], type)
        return self.cards[index]

    def get_all(self, type: Type[C] = Card) -> List[C]:
        result: List[type] = []
        hands: List[Card] = self.cards
        if type == Card:
            return hands
        for c in hands:
            if isinstance(c, type):
                result.append(c)
        return result
