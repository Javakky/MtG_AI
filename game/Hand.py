from typing import List, Type, TypeVar

from game.card.Card import Card
from util.util import assert_instanceof


class Hand:
    C = TypeVar('C', bound=Card)
    cards: List[Card] = []

    def append(self, card: Card):
        self.cards.append(card)

    def pop(self, index: int, type: Type[C] = Card) -> C:
        assert_instanceof(self.cards[index], type)
        return self.cards.pop(index)

    def get(self, index: int, type: Type[C] = Card) -> C:
        assert_instanceof(self.cards[index], type)
        return self.cards[index]
