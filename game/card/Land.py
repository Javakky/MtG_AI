from game.card.CardType import CardType
from game.card.ManaBase import ManaBase
from game.mana.Mana import Mana


class Land(ManaBase):

    def __init__(self, name: str, mana: Mana):
        super().__init__(name, mana)

    def type(self) -> CardType:
        return CardType.LAND

    def __str__(self) -> str:
        return "【" + self.name + "】" + " " + self.type().value + "： " + \
               self.mana.__str__() + \
               (" (T)" if not self.untapped else "")
