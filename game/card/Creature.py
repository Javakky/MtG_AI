import copy
from typing import List

from game.card.CardType import CardType
from game.card.Permanent import Permanent
from game.card.Spell import Spell
from game.mana.Mana import Mana


class Creature(Permanent, Spell):

    def __init__(self, name: str, cost: Mana, creature_type: List[str], power: int, toughness: int):
        super().__init__(name)
        self.mana_cost = cost
        self.creature_type: List[str] = creature_type
        self.power: int = power
        self.toughness: int = toughness

    def type(self) -> CardType:
        return CardType.CREATURE

    def __str__(self) -> str:
        return "【" + self.name + "】" + " " + self.type().value + "：　" + \
               str(self.power) + "/" + str(self.toughness) + " (" + self.mana_cost.__str__() + ")" + \
               (" (T)" if not self.untapped else "")

    def clone(self) -> 'Creature':
        return Creature(self.name, self.mana_cost.clone(), copy.deepcopy(self.creature_type), self.power,
                        self.toughness)
