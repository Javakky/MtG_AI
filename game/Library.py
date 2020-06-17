import random
from typing import List, Optional

from game.card.Card import *


class Library:
    cards: List[Card]

    def __init__(self, deck: List[Card]):
        self.cards = deck

    def pop(self) -> Optional[Card]:
        if len(self.cards) < 1:
            return None
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)
