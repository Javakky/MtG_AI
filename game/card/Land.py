from game.card.ManaBase import ManaBase
from game.mana.Mana import Mana


class Land(ManaBase):

    def __init__(self, name: str, mana: Mana):
        super().__init__(name, mana)

    def type(self):
        return "Land"

    def __str__(self) -> str:
        return "【" + self.name + "】" + " " + self.type() + "： " + \
               self.mana.__str__() + \
               (" (T)" if not self.untapped else "")
