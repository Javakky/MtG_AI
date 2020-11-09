from typing import Dict

from game.card.Card import Card


class CardPool:
    pool: Dict[str, Card]

    def add_card(self, value: Card):
        self.pool[value.name] = value
