from abc import ABCMeta
from typing import Optional

from game.card.Permanent import Permanent
from game.mana.Mana import Mana


class ManaBase(Permanent, metaclass=ABCMeta):
    def __init__(self, name: str, mana: Mana):
        super().__init__(name)
        self.mana: Mana = mana

    def addable_symbols(self) -> Mana:
        return self.mana

    def add_symbols(self) -> Optional[Mana]:
        if not self.untapped:
            return None
        self.tap()
        return self.mana
