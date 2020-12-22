from typing import List, Tuple

from client.console_user import ConsoleUser
from games.cards.creature import Creature
from games.cards.land import Land
from util.util import debug_print, debug_print_cards


def require_land(creature: Creature, lands: List[Tuple[int, Land]]):
    land_indexes: List[Tuple[int, Land]] = []
    generated_mana: int = 0
    creature_mana: int = creature.mana_cost.count()
    for land in lands:
        if creature_mana > generated_mana:
            land_indexes.append(land)
            generated_mana += land[1].mana.count()
    return land_indexes


class AI(ConsoleUser):
    def play_land(self) -> bool:
        lands: List[Tuple[int, Land]] = self.game.get_indexed_hands(self, Land)
        if not self.game.played_land() and lands.__len__() > 0:
            debug_print("【" + self.name + "】が土地をプレイしました：")
            debug_print_cards([lands[0][1]])
            self.game.play_land(lands[0][0])
            return True
        return False
