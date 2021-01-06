import random
from typing import List, Optional

from games.card_holder import CardHolder
from games.cards.card import *


class Library(CardHolder):

    def append(self, card):
        self.cards.append(card)

    def __init__(self, deck: List[Card]):
        self.cards: List[Card] = deck

    def pop(self, name: str = None) -> Optional[Card]:
        if name is None:
            if len(self.cards) < 1:
                return None
            return self.cards.pop()
        for card in self.cards:
            if card.name == name:
                self.cards.remove(card)
                return card
        return None

    def shuffle(self):
        random.shuffle(self.cards)
