import random
from itertools import combinations
from typing import List, Dict, Tuple, Iterator

from ai.ai import require_land, AI
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from util.util import debug_print, get_keys_tuple_list, get_values_tuple_list, debug_print_cards, \
    debug_print_cards_of_index


def all_playable_creature(creatures: List[Tuple[int, Creature]], mana_cost: int) \
        -> List[List[Tuple[int, Creature]]]:
    result: List[List[Tuple[int, Creature]]] = []
    for i in reversed(range(0, creatures.__len__() + 1)):
        comb: Iterator[Tuple[Tuple[int, Creature], ...]] = combinations(creatures, i)
        for tuple in comb:
            if sum([x[1].mana_cost.count() for x in tuple]) <= mana_cost:
                result.append(list(tuple))
    return result


def all_attackable_creature(creatures: List[Tuple[int, Creature]]) \
        -> List[List[Tuple[int, Creature]]]:
    result: List[List[Tuple[int, Creature]]] = []
    for i in reversed(range(0, creatures.__len__() + 1)):
        comb: Iterator[Tuple[Tuple[int, Creature], ...]] = combinations(creatures, i)
        for tuple in comb:
            result.append(list(tuple))
    return result


class RandomPlayer(AI):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)
        self.played_land: bool = False
        self.selected_spell: bool = False
        self.selected: List[Tuple[int, Creature]] = []

    def get_deck(self) -> List[Card]:
        return get_sample_deck()

    def choose_play_first(self):
        self.game.choose_play_first(self, True)

    def draw_starting_hand(self, hands: List[Card]):
        debug_print("【" + self.name + "】の初期手札 " + str(len(hands)) + "枚：")
        debug_print_cards(hands)
        debug_print()

    def chosen_play_first(self, play_first: bool):
        pass

    def upkeep_step(self):
        debug_print("ターン" + str(self.game.turn) + "：" + self.name)
        self.played_land = False
        self.selected_spell = False
        self.selected = []

    def draw_step(self, card: Card):
        self.debug_print_hand()
        self.game.finish_main_phase()

    def combat_damage(self, result: Dict):
        debug_print(result)

    def ending_the_game(self, win: bool):
        debug_print("【" + self.name + "】は" + ("勝利" if win else "敗北") + "しました")

    def receive_priority(self):
        if not self.played_land:
            self.played_land = True
            if bool(random.getrandbits(1)) and self.play_land():
                return
        if self.selected_spell:
            if self.selected.__len__() > 0:
                creature: Tuple[int, Creature] = self.selected.pop(0)
                lands: List[Tuple[int, Land]] = self.game.get_indexed_fields(self, True, type=Land)
                land_indexes: List[Tuple[int, Creature]] = require_land(creature[1], lands)
                self.debug_print_field()
                debug_print("【" + self.name + "】がクリーチャーをプレイしました：")
                debug_print_cards([creature[1]])
                debug_print("土地をタップしました：")
                debug_print_cards(get_values_tuple_list(land_indexes))
                self.game.cast_pay_cost(creature[0], get_keys_tuple_list(land_indexes))
            else:
                self.game.pass_priority()
        else:
            self.selected_spell = True
            playable: List[List[Tuple[int, Creature]]] = all_playable_creature(
                self.game.get_indexed_hands(self, Creature),
                self.game.get_remain_mana().count()
            )
            self.selected = playable[random.randint(0, playable.__len__() - 1)]
            self.selected = sorted(self.selected, key=lambda x: x[0], reverse=True)
            self.receive_priority()

    def declare_attackers_step(self):
        P_A: List[Tuple[int, Creature]] = sorted(
            self.game.get_indexed_fields(self, True, Creature),
            key=lambda x: (x[1].power, x[1].mana_cost.count())
        )
        if P_A.__len__() == 0:
            self.game.declare_attackers([])
            return

        debug_print_cards(self.game.get_fields(self.game.non_self_users(self)[0], True, Creature))
        attackable: List[List[Tuple[int, Creature]]] = all_attackable_creature(P_A)
        self.game.declare_attackers(get_keys_tuple_list(attackable[random.randint(0, attackable.__len__() - 1)]))

    def declare_blockers_step(self, P_A_index: List[int]):
        P_A: List[Tuple[int, Tuple[int, Creature]]] = []
        for i in range(P_A_index.__len__()):
            P_A.append(
                (i, (P_A_index[i], self.game.get_field(self.game.non_self_users(self)[0], P_A_index[i], Creature)))
            )
        P_A = sorted(P_A, key=lambda x: (x[1][1].power, x[1][1].mana_cost.count()))
        debug_print("アタッカー:")
        debug_print_cards_of_index(get_values_tuple_list(P_A))
        P_B: List[Tuple[int, Creature]] = self.game.get_indexed_fields(self, True, Creature)
        # debug_print("潜在的ブロッカー:")
        # debug_print_cards_of_index(P_B)
        if P_B.__len__() == 0:
            self.game.combat_damage()
            return

        B: List[List[Tuple[int, Creature]]] = [[] for i in range(P_A.__len__())]

        for b in P_B:
            rand = random.randint(0, P_A.__len__())
            if rand == P_A.__len__():
                continue
            B[P_A[rand][0]].append(b)

        debug_print("選択結果：")
        for i in range(P_A.__len__()):
            debug_print(str(i) + ":")
            debug_print_cards_of_index(B[i])
            self.game.declare_blokers(i, get_keys_tuple_list(B[i]))
        self.game.combat_damage()
