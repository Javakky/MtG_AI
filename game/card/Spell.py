from abc import ABCMeta
from typing import Optional

from game.card.Card import Card
from game.mana.Mana import Mana


class Spell(Card, metaclass=ABCMeta):

    def __init__(self, name: str):
        super().__init__(name)
        self.mana_cost: Optional[Mana] = None

    def legal_mana_cost(self, mana: Mana) -> bool:
        return mana.contains(self.mana_cost)
