from itertools import combinations
from typing import List, Tuple, Union, NoReturn

from client.console_user import ConsoleUser
from games.cards.creature import Creature
from games.cards.land import Land
from util.util import debug_print, debug_print_cards, index_with_default, combinations_all


def require_land(creature: Creature, lands: List[Tuple[int, Land]]) -> List[Tuple[int, Land]]:
    land_indexes: List[Tuple[int, Land]] = []
    generated_mana: int = 0
    creature_mana: int = creature.mana_cost.count()
    for land in lands:
        if creature_mana > generated_mana:
            land_indexes.append(land)
            generated_mana += land[1].mana.count()
    return land_indexes


def find_damage_destroyable_max_cost_assign(point: int, B: List[Tuple[int, Creature]]) -> List[int]:
    _b = list(filter(lambda x: x[1].toughness <= point, B))
    result: List[Tuple[int, Creature]] = []
    max_cost: int = 0
    max_count: int = 0
    for i in range(1, _b.__len__() + 1):
        comb: List[Tuple[Tuple[int, Creature], ...]] = list(combinations(_b, i))
        for c in comb:
            if sum([x[1].toughness for x in c]) <= point:
                cost: int = sum([x[1].mana_cost.count() for x in c])
                count: int = c.__len__()
                if cost > max_cost or cost == max_cost and count >= max_count:
                    max_cost = cost
                    max_count = count
                    result = list(c)
    assign: List[int] = [0 for x in B]
    for r in result:
        index: Union[int, False] = index_with_default(B, r)
        if index is not False:
            assign[index] = r[1].toughness
    return assign


class AI(ConsoleUser):
    def play_land(self) -> bool:
        lands: List[Tuple[int, Land]] = self.game.get_indexed_hands(self, Land)
        if not self.game.played_land() and lands.__len__() > 0:
            debug_print("【" + self.name + "】が土地をプレイしました：")
            debug_print_cards([lands[0][1]])
            self.game.play_land(lands[0][0])
            return True
        return False

    def assign_damage(self, attacker: int, blockers: List[int]) -> NoReturn:
        point: int = self.game.get_field(self, attacker, Creature).power
        _b: List[Tuple[int, Creature]] = [(x, self.game.get_field(self.game.non_self_users(self)[0], x, Creature))
                                          for x in blockers]
        self.game.assign_damage(attacker, blockers, find_damage_destroyable_max_cost_assign(point, _b))


def all_playable_pairs(
        creatures: List[Tuple[int, Creature]], remain_mana: int
) \
        -> List[List[Tuple[int, Creature]]]:
    playable_creatures: List[List[Tuple[int, Creature]]] = combinations_all(
        creatures,
        1,
        lambda c: sum([creature[1].mana_cost.count() for creature in c]) <= remain_mana
    )
    return playable_creatures


def maximam_playable_pairs(creatures: List[Tuple[int, Creature]], remain_mana: int) \
        -> List[List[Tuple[int, Creature]]]:
    playable_pairs: List[List[Tuple[int, Creature]]] = all_playable_pairs(creatures, remain_mana)

    result: List[List[Tuple[int, Creature]]] = []

    for pair in playable_pairs:
        for r in result:
            for creature in pair:
                if creature not in r:
                    break
            else:
                break
        else:
            result.append(pair)

    return result
