from typing import List, Type, TypeVar, Optional, NoReturn

from games.card_holder import CardHolder
from games.cards.card import Card
from util.util import assert_instanceof


class Hand(CardHolder):
    C = TypeVar('C', bound=Card)

    def __init__(self):
        self.cards: List[Card] = []

    def append(self, card: Card) -> NoReturn:
        self.cards.append(card)

    def pop(self, name: str) -> Optional[Card]:
        if name is None:
            raise NotImplementedError
        for card in self.cards:
            if card.name == name:
                self.cards.remove(card)
                return card
        return None

    def pop_index(self, index: int, type: Type[C] = Card) -> C:
        assert_instanceof(self.cards[index], type)
        return self.cards.pop(index)

    def pop_all(self) -> List[Card]:
        cards: List[Card] = self.cards
        self.cards = []
        return cards

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

    def set_all(self, cards: List[Card]) -> NoReturn:
        self.pop_all()
        for card in cards:
            self.append(card)
