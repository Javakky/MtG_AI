from typing import List

from games.cards.card import Card


class Graveyard:
    def __init__(self):
        self.cards: List[Card] = []

    def append(self, card: Card):
        self.cards.append(card)
