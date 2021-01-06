import copy
from typing import List, Set

from games.cards.card_type import CardType
from games.cards.permanent import Permanent
from games.cards.spell import Spell
from games.mana.mana import Mana


class Creature(Permanent, Spell):

    def has_type(self, card_type: CardType) -> bool:
        return card_type == self.type()

    def __init__(self, name: str, cost: Mana, creature_type: List[str], power: int, toughness: int):
        super().__init__(name)
        self.mana_cost: Mana = cost
        self.creature_type: Set[str] = set(creature_type)
        self.power: int = power
        self.toughness: int = toughness

    def type(self) -> CardType:
        return CardType.CREATURE

    def __str__(self) -> str:
        return "【" + self.name + "】" + " " + self.type().value + "：　" + \
               str(self.power) + "/" + str(self.toughness) + " (" + self.mana_cost.__str__() + ")" + \
               (" (T)" if not self.untapped else "")

    def clone(self) -> 'Creature':
        return Creature(self.name, self.mana_cost.clone(), copy.deepcopy(list(self.creature_type)), self.power,
                        self.toughness)
