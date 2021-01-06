from typing import List, Type, TypeVar, Optional

from games.card_holder import CardHolder
from games.cards.card import Card


class Graveyard(CardHolder):
    C = TypeVar('C', bound=Card)

    def __init__(self):
        self.cards: List[Card] = []

    def append(self, card: Card):
        self.cards.append(card)

    def get(self, index: int, type: Type[C] = Card) -> C:
        assert_instanceof(self.cards[index], type)
        return self.cards[index]

    def get_all(self, type: Type[C] = Card) -> List[C]:
        result: List[type] = []
        graveyards: List[Card] = self.cards
        if type == Card:
            return graveyards
        for c in graveyards:
            if isinstance(c, type):
                result.append(c)
        return result

    def pop(self, name: str) -> Optional[Card]:
        if name is None:
            return self.cards.pop(self.cards.__len__() - 1)
        for card in self.cards:
            if card.name == name:
                self.cards.remove(card)
                return card
        return None
