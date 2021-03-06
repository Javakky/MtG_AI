from itertools import combinations
from typing import List, Dict, Optional, cast, Tuple, Iterator, Callable, NoReturn

from ai.ai import require_land, AI
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from games.mana.mana import Mana
from util.util import debug_print, get_keys_tuple_list, get_values_tuple_list, debug_print_cards


def exists_one_sidedly_destroied_pair(p_A: Creature, p_B: List[Creature]) -> bool:
    power: int = 0
    for b in p_B:
        if b.toughness > p_A.power:
            power += b.power
        if power >= p_A.toughness:
            return True
    return False


def exists_exchanged_low_cost_pair(p_A: Creature, P_B: List[Creature]) -> bool:
    one_sidedlies_power: int = 0
    not_one_sidedlies: List[Creature] = []
    for b in P_B:
        if b.toughness > p_A.power:
            one_sidedlies_power += b.power
        else:
            not_one_sidedlies.append(b)
    for b in not_one_sidedlies:
        if b.mana_cost.count() < p_A.mana_cost.count() \
                and b.power + one_sidedlies_power >= p_A.toughness:
            return True
    return False


def exists_exchange_high_cost_next_turn(p_A: Creature, P_B: List[Creature]) -> bool:
    for b in P_B:
        if p_A.power >= b.toughness and p_A.mana_cost.count() < b.mana_cost.count():
            return True
    return False


def find_one_sidedly_destroied_smaller_cost_pair(p_A: Creature, p_B: List[Tuple[int, Creature]]) \
        -> List[Tuple[int, Creature]]:
    return find_exchanged_creature_pair(p_A, p_B, lambda x: x[1].toughness > p_A.power)


def find_exchanged_low_cost_creature(p_A: Creature, P_B: List[Tuple[int, Creature]]) \
        -> List[Tuple[int, Creature]]:
    P_B = sorted(P_B, key=lambda x: x[1].mana_cost.count())
    for b in P_B:
        if b[1].mana_cost.count() >= p_A.mana_cost.count():
            continue
        if b[1].power >= p_A.toughness:
            return [b]
    return []


def find_pair_exchanged_low_cost_creature(p_A: Creature, P_B: List[Tuple[int, Creature]]) \
        -> List[Tuple[int, Creature]]:
    P_B = sorted(P_B, key=lambda x: x[1].mana_cost.count())
    L: List[Tuple[Tuple[int, Creature]]] = list(combinations(P_B, 2))
    max_cost: int = P_B[P_B.__len__() - 1][1].mana_cost.count() * 2 + 1
    result: List[Tuple[int, Creature]] = []
    for pair in L:
        power: int = 0
        toughness: int = 0
        cost: int = 0
        for p_B in pair:
            power += p_B[1].power
            toughness += p_B[1].toughness
            if cost > p_B[1].mana_cost.count():
                cost = p_B[1].mana_cost.count()
            if p_B[1].toughness >= p_A.power:
                if p_B[1].mana_cost.count() <= p_A.mana_cost.count():
                    break
        if power >= p_A.toughness and toughness > p_A.power and cost <= max_cost:
            result = list(pair)
            max_cost = cost
    return result


def maximum_playable_creature_count_enough_land(creatures: List[Creature], lands_of_hands: List[Land],
                                                remain_mana: int) -> int:
    land_mana: Mana = Mana([]) if lands_of_hands.__len__() == 0 else lands_of_hands[0].mana
    remain_mana_count: int = remain_mana + land_mana.count()
    for i in reversed(range(1, creatures.__len__() + 1)):
        comb: Iterator[Tuple[Creature, ...]] = combinations(creatures, i)
        for tuple in comb:
            if sum([x.mana_cost.count() for x in tuple]) <= remain_mana_count:
                return i
    return 0


def count_smallest_pair_exceeds_my_life(P_A: List[Creature], life: int) -> int:
    P_A = sorted(P_A, key=lambda x: (x.power, x.mana_cost.count()))
    power: int = 0
    for i in range(P_A.__len__()):
        power += P_A[i].power
        if life <= power:
            return P_A.__len__() - i
    return 0


def find_not_exchanged_creature(P_A: Creature, P_B: List[Tuple[int, Creature]]) -> List[Tuple[int, Creature]]:
    P_B = sorted(P_B, key=lambda x: (x[1].mana_cost.count()))
    for b in P_B:
        if P_A.power < b[1].toughness:
            return [b]
    return []


def find_exchanged_creature_pair(
        p_A: Creature, p_B: List[Tuple[int, Creature]],
        filter_func: Optional[Callable[[Tuple[int, Creature]], bool]] = None
) -> List[Tuple[int, Creature]]:
    if filter_func is None:
        filter_func = lambda x: True
    L: List[Tuple[int, Creature]] = sorted(list(filter(filter_func, p_B)),
                                           key=lambda x: (x[1].power, x[1].mana_cost.count()))
    min_cost: int = sum([x[1].mana_cost.count() for x in L]) + 1
    min_count: int = L.__len__() + 1
    result: List[Tuple[int, Creature]] = []
    for i in range(1, L.__len__() + 1):
        comb: List[Tuple[Tuple[int, Creature], ...]] = list(combinations(L, i))
        for c in comb:
            if sum([x[1].power for x in c]) >= p_A.toughness:
                cost: int = sum([x[1].mana_cost.count() for x in c])
                count: int = c.__len__()
                if cost < min_cost or cost == min_count and count <= min_count:
                    min_cost = cost
                    min_count = count
                    result = list(c)
    return result


class Expert(AI):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)

    def get_deck(self) -> List[Card]:
        # return get_random_deck()
        return get_sample_deck()
        # return get_minimum_deck()

    def choose_play_first(self) -> NoReturn:
        self.game.choose_play_first(self, True)

    def draw_starting_hand(self, hands: List[Card]) -> NoReturn:
        debug_print("【" + self.name + "】の初期手札 " + str(len(hands)) + "枚：")
        debug_print_cards(hands)
        debug_print()

    def chosen_play_first(self, play_first: bool) -> NoReturn:
        pass

    def upkeep_step(self) -> NoReturn:
        debug_print("ターン" + str(self.game.turn) + "：" + self.name)

    def draw_step(self, card: Card) -> NoReturn:
        self.debug_print_hand()

    def combat_damage(self, result: Dict) -> NoReturn:
        debug_print(result)

    def ending_the_game(self, win: bool) -> NoReturn:
        debug_print("【" + self.name + "】は" + ("勝利" if win else "敗北") + "しました")

    def _play_spell(self) -> List[Tuple[int, Creature]]:
        result: List[Tuple[int, Creature]] = []
        creatures: List[Tuple[int, Creature]] = self.game.get_indexed_hands(self, Creature)
        remain_mana: int = self.game.get_remain_mana()
        while True:
            most_large_cost_creature: Optional[Tuple[int, Creature]] = None
            for tpl in creatures:
                if tpl[1].mana_cost.count() <= remain_mana and \
                        (most_large_cost_creature is None
                         or most_large_cost_creature[1].mana_cost.count() < tpl[1].mana_cost.count()):
                    most_large_cost_creature = tpl
            if most_large_cost_creature is None:
                break
            result.append(most_large_cost_creature)
            creatures.remove(most_large_cost_creature)
            remain_mana -= most_large_cost_creature[1].mana_cost.count()
        return result

    def _play_land(self) -> Optional[int]:
        lands: List[Tuple[int, Land]] = self.game.get_indexed_hands(self, Land)
        if lands.__len__() > 0:
            return lands[0][0]
        return None

    def receive_priority(self) -> NoReturn:
        if self.play_land():
            return
        creatures: List[Tuple[int, Creature]] = self.game.get_indexed_hands(self, Creature)
        lands: List[Tuple[int, Land]] = self.game.get_indexed_fields(self, True, type=Land)
        remain_mana: int = self.game.get_remain_mana()
        most_large_cost_creature: Optional[Creature] = None
        creature_index: int = -1
        for tpl in creatures:
            if tpl[1].mana_cost.count() <= remain_mana and \
                    (most_large_cost_creature is None
                     or most_large_cost_creature.mana_cost.count() < tpl[1].mana_cost.count()):
                most_large_cost_creature = cast(Creature, tpl[1])
                creature_index = tpl[0]
        if most_large_cost_creature is not None:
            land_indexes: List[Tuple[int, Land]] = require_land(most_large_cost_creature, lands)
            self.debug_print_field()
            debug_print("【" + self.name + "】がクリーチャーをプレイしました：")
            debug_print_cards([most_large_cost_creature])
            debug_print("土地をタップしました：")
            debug_print_cards(get_values_tuple_list(land_indexes))
            self.game.cast_pay_cost(creature_index, get_keys_tuple_list(land_indexes))
        else:
            self.game.pass_priority()

    def _declare_attackers_step(self, P_A: Optional[List[Tuple[int, Creature]]] = None,
                                A: Optional[List[Tuple[int, Creature]]] = None) -> List[int]:
        if P_A is None:
            P_A: List[Tuple[int, Creature]] = sorted(
                self.game.get_indexed_fields(self, True, Creature),
                key=lambda x: (x[1].power, x[1].mana_cost.count())
            )
        if P_A.__len__() == 0:
            return []

        P_B: List[Creature] = sorted(
            self.game.get_fields(self.game.non_self_users(self)[0], True, Creature),
            key=lambda x: (x.power, x.mana_cost.count())
        )
        if P_B.__len__() == 0:
            return get_keys_tuple_list(P_A)

        d: int = P_A.__len__() - P_B.__len__()
        if d == 0 and \
                sum([x[1].power for x in P_A]) >= self.game.get_life(self.game.non_self_users(self)[0]):
            return get_keys_tuple_list(P_A)

        a_max = P_A.__len__() \
                + maximum_playable_creature_count_enough_land(
            self.game.get_hands(self, Creature),
            self.game.get_hands(self, Land),
            self.game.get_remain_mana()
        ) \
                - count_smallest_pair_exceeds_my_life(
            self.game.get_fields(self.game.non_self_users(self)[0], type=Creature),
            self.game.get_life(self)
        )
        if a_max == 0:
            return []
        if a_max < 0:
            return get_keys_tuple_list(P_A)

        if A is None:
            A: List[int] = []
        else:
            A: List[int] = get_keys_tuple_list(A)
        i: int = P_A.__len__() - 1
        while A.__len__() < a_max and i > 0:
            if not exists_one_sidedly_destroied_pair(P_A[i][1], P_B) \
                    and not exists_exchanged_low_cost_pair(P_A[i][1], P_B) \
                    and not exists_exchange_high_cost_next_turn(P_A[i][1], P_B):
                A.append(P_A[i][0])
                pass
            i -= 1
        return A

    def declare_attackers_step(self, P_A: Optional[List[Tuple[int, Creature]]] = None,
                               A: Optional[List[Tuple[int, Creature]]] = None) -> NoReturn:
        A: List[int] = self._declare_attackers_step(P_A, A)
        self.game.declare_attackers(A)
        return

    def _declare_blockers_step(self, P_A_index: List[int],
                               P_B: Optional[List[Tuple[int, Creature]]] = None,
                               b: Optional[List[Tuple[int, Tuple[int, Creature]]]] = None) -> List[
        List[Tuple[int, Creature]]]:
        P_A: List[Tuple[int, Tuple[int, Creature]]] = []
        for i in range(P_A_index.__len__()):
            P_A.append(
                (i, (P_A_index[i], self.game.get_field(self.game.non_self_users(self)[0], P_A_index[i], Creature)))
            )
        P_A = sorted(P_A, key=lambda x: (x[1][1].power, x[1][1].mana_cost.count()))
        if P_B is None:
            P_B: List[Tuple[int, Creature]] = self.game.get_indexed_fields(self, True, Creature)
        if P_B.__len__() == 0:
            return []

        b_min: int = 0 if sum([x[1][1].power for x in P_A]) < self.game.get_life(self) \
            else count_smallest_pair_exceeds_my_life(get_values_tuple_list(get_values_tuple_list(P_A)),
                                                     self.game.get_life(self))

        if b_min > P_A.__len__():
            return []

        i: int = P_A.__len__() - 1
        B: List[List[Tuple[int, Creature]]] = [[] for i in range(P_A.__len__())]
        if b is not None:
            for _b in b:
                if _b[0] < P_A.__len__():
                    B[_b[0]].append(_b[1])
        while P_B.__len__() != 0 and i >= 0:
            for _ in [0]:
                b: List[Tuple[int, Creature]] = find_one_sidedly_destroied_smaller_cost_pair(P_A[i][1][1], P_B)

                if b.__len__() > 0:
                    B[P_A[i][0]] = b
                    break

                b = find_exchanged_low_cost_creature(P_A[i][1][1], P_B)

                if b.__len__() > 0:
                    B[P_A[i][0]] = b
                    break

                b = find_not_exchanged_creature(P_A[i][1][1], P_B)

                if b.__len__() > 0:
                    B[P_A[i][0]] = b
                    break

                if i > P_A.__len__() - b_min:
                    b = find_exchanged_creature_pair(P_A[i][1][1], P_B)

                    if b.__len__() > 0:
                        B[P_A[i][0]] = b
                    else:
                        B[P_A[i][0]] = [sorted(P_B, key=lambda x: x[1].mana_cost.count())[0]]

            P_B = list(set(P_B) ^ set(B[P_A[i][0]]))
            i -= 1
        return B

    def declare_blockers_step(self, P_A_index: List[int],
                              P_B: Optional[List[Tuple[int, Creature]]] = None,
                              b: Optional[List[Tuple[int, Tuple[int, Creature]]]] = None) -> NoReturn:
        B: List[List[Tuple[int, Creature]]] = self._declare_blockers_step(P_A_index, P_B, b)
        for i in range(B.__len__()):
            self.game.declare_blokers(i, get_keys_tuple_list(B[i]))
        self.game.combat_damage()
