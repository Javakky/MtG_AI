import random
from typing import List, Optional

from games.cards.card import *


class Library:

    def __init__(self, deck: List[Card]):
        self.cards: List[Card] = deck

    def pop(self) -> Optional[Card]:
        if len(self.cards) < 1:
            return None
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)
