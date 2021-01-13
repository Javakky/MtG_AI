import json
from typing import List, Dict, NoReturn, cast, Tuple

from ai.ai import AI, require_land
from ai.montecalro.sample_game import SampleGame
from ai.montecalro.timing import Timing
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from util.montecalro.mtcs import monte_carlo_tree_search_next_action
from util.util import get_keys_tuple_list


class PA(AI):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)
        self.selected_spell: bool = False
        self.selected: List[Tuple[int, Creature]] = []

    def get_deck(self) -> List[Card]:
        return get_sample_deck()

    def choose_play_first(self) -> NoReturn:
        self.game.choose_play_first(self, True)

    def draw_starting_hand(self, hands: List[Card]) -> NoReturn:
        pass

    def chosen_play_first(self, play_first: bool) -> NoReturn:
        pass

    def upkeep_step(self) -> NoReturn:
        self.selected_spell = False
        self.selected = []

    def draw_step(self, card: Card) -> NoReturn:
        pass

    def receive_priority(self) -> NoReturn:
        if not self.game.played_land():
            params: Dict[str, object] = monte_carlo_tree_search_next_action(
                SampleGame(self, Timing.SELECT_BLOCKER)
            ).next_params
            if "land" in params:
                print("land: " + str(params["land"]))
                self.game.play_land(cast(int, params["land"]))
                return
        if self.selected_spell:
            if self.selected.__len__() > 0:
                creature: Tuple[int, Creature] = self.selected.pop(0)
                lands: List[Tuple[int, Land]] = self.game.get_indexed_fields(self, True, type=Land)
                land_indexes: List[Tuple[int, Land]] = require_land(creature[1], lands)
                self.game.cast_pay_cost(creature[0], get_keys_tuple_list(land_indexes))
            else:
                self.game.pass_priority()
        else:
            self.selected_spell = True
            params: Dict[str, object] = monte_carlo_tree_search_next_action(
                SampleGame(self, Timing.PLAY_LAND)
            ).next_params
            if "spell" in params:
                self.selected = cast(List[Tuple[int, Creature]], params["spell"])
                self.selected = sorted(self.selected, key=lambda x: x[0], reverse=True)
                print("spell: " + json.dumps(get_keys_tuple_list(self.selected)))
            self.receive_priority()

    def declare_attackers_step(self) -> NoReturn:
        params: Dict[str, object] = monte_carlo_tree_search_next_action(
            SampleGame(self, Timing.AFTER_START)
        ).next_params
        if "attacker" in params:
            print("attacker: " + json.dumps(params["attacker"]))
            self.game.declare_attackers(cast(List[int], params["attacker"]))
        else:
            self.game.declare_attackers([])

    def declare_blockers_step(self, attackers: List[int]) -> NoReturn:
        if self.game.tmp_attacker.__len__() == 0:
            self.game.combat_damage()
            return
        game: SampleGame = SampleGame(self, Timing.SELECT_ATTACKER)
        params: Dict[str, object] = monte_carlo_tree_search_next_action(
            game
        ).next_params
        if "blocker" in params:
            print("attacker: " + json.dumps(params["blocker"]))
            blockers: List[List[int]] = cast(List[List[int]], params["blocker"])
            for i in range(blockers.__len__()):
                self.game.declare_blokers(i, blockers[i])
        self.game.combat_damage()

    def combat_damage(self, result: Dict) -> NoReturn:
        pass

    def ending_the_game(self, win: bool) -> NoReturn:
        print("経過ターン数: " + str(self.game.turn))
        print("相手のライフ: " + str(self.game.get_life(self)))
        print("自分のライフ: " + str(self.game.get_life(self.game.non_self_users(self)[0])))
        self.print_field(True)
