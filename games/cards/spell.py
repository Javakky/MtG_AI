from abc import ABCMeta
from typing import Optional

from games.cards.card import Card
from games.mana.mana import Mana


class Spell(Card, metaclass=ABCMeta):

    def __init__(self, name: str):
        super().__init__(name)
        self.mana_cost: Optional[Mana] = None

    def legal_mana_cost(self, mana: Mana) -> bool:
        return mana.contains(self.mana_cost)
