from games.cards.card_type import CardType
from games.cards.mana_base import ManaBase
from games.mana.mana import Mana


class Land(ManaBase):

    def has_type(self, card_type: CardType) -> bool:
        return card_type == self.type()

    def __init__(self, name: str, mana: Mana):
        super().__init__(name, mana)

    def type(self) -> CardType:
        return CardType.LAND

    def __str__(self) -> str:
        return "【" + self.name + "】" + " " + self.type().value + "： " + \
               self.mana.__str__() + \
               (" (T)" if not self.untapped else "")

    def clone(self) -> 'Land':
        return Land(self.name, self.mana.clone())
