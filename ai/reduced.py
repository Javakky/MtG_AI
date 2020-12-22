import random
from typing import List, Dict, Tuple

from ai.ai import require_land, AI
from ai.expert import find_damage_destroyable_max_cost_assign
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from games.mana.mana import Mana
from util.util import debug_print, get_keys_tuple_list, get_values_tuple_list, debug_print_cards, \
    debug_print_cards_of_index


class Reduced(AI):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)

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

    def draw_step(self, card: Card):
        self.debug_print_hand()
        self.game.finish_main_phase()

    def combat_damage(self, result: Dict):
        debug_print(result)

    def ending_the_game(self, win: bool):
        debug_print("【" + self.name + "】は" + ("勝利" if win else "敗北") + "しました")

    def receive_priority(self):
        if self.play_land():
            return
        remain_mana: Mana = self.game.get_remain_mana()
        creatures: List[Tuple[int, Creature]] = list(filter(
            lambda x: (x[1].mana_cost.count() < remain_mana.count()),
            self.game.get_indexed_hands(self, Creature)))
        lands: List[Tuple[int, Land]] = self.game.get_indexed_fields(self, True, type=Land)
        if creatures.__len__() > 0:
            creature: Tuple[int, Creature] = creatures[random.randint(0, creatures.__len__() - 1)]
            land_indexes: List[Tuple[int, Creature]] = require_land(creature[1], lands)
            self.debug_print_field()
            debug_print("【" + self.name + "】がクリーチャーをプレイしました：")
            debug_print_cards([creature[1]])
            debug_print("土地をタップしました：")
            debug_print_cards(get_values_tuple_list(land_indexes))
            self.game.cast_pay_cost(creature[0], get_keys_tuple_list(land_indexes))
        else:
            self.game.pass_priority()

    def declare_attackers_step(self):
        P_A: List[Tuple[int, Creature]] = sorted(
            self.game.get_indexed_fields(self, True, Creature),
            key=lambda x: (x[1].power, x[1].mana_cost.count())
        )
        if P_A.__len__() == 0:
            self.game.declare_attackers([])
            return

        debug_print_cards(self.game.get_fields(self.game.non_self_users(self)[0], True, Creature))
        A: List[int] = []
        for i in range(P_A.__len__()):
            if random.random() >= 0.5:
                A.append(P_A[i][0])
        self.game.declare_attackers(A)

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

    def assign_damage(self, attacker: int, blockers: List[int]):
        point: int = self.game.get_field(self, attacker, Creature).power
        _b: List[Tuple[int, Creature]] = [(x, self.game.get_field(self.game.non_self_users(self)[0], x, Creature))
                                          for x in blockers]
        self.game.assign_damage(attacker, blockers, find_damage_destroyable_max_cost_assign(point, _b))
