from typing import List

from game.card.Card import Card


class Graveyard:
    cards: List[Card] = []

    def append(self, card: Card):
        self.cards.append(card)
