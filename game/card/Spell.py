from game.card.Card import Card
from game.mana.Mana import Mana


class Spell(Card):
    mana_cost: Mana

    def legal_mana_cost(self, mana: Mana) -> bool:
        return mana.contains(self.mana_cost)
