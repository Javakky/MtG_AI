from typing import List, Dict, NoReturn, cast, Tuple, Optional

from ai.ai import AI, require_land
from ai.montecalro.mtg_config import MtGConfig
from ai.montecalro.sample_game import SampleGame
from ai.montecalro.timing import Timing
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from util.montecalro.mcts import MCTS
from util.util import get_keys_tuple_list


class MCTS_AI(AI):

    def __init__(self, game: Game, name: str, config: MtGConfig):
        super().__init__(game, name)
        self.played_land: bool = False
        self.selected_spell: bool = False
        self.selected: List[Tuple[int, Creature]] = []
        self.config: MtGConfig = config
        self.mcts: MCTS = MCTS(config)
        self.binary_wait: List[Tuple[int, Creature]] = []
        self.binary_playing: bool = False

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
        self.played_land = False
        self.selected = []
        self.binary_playing = False

    def draw_step(self, card: Card) -> NoReturn:
        pass

    def receive_priority(self) -> NoReturn:
        if not self.played_land:
            self.played_land = True
            params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
                SampleGame(self, Timing.BEFORE_LAND, self.config),
                self.config
            ).next_params
            if "land" in params:
                self.game.play_land(cast(int, params["land"]))
                return

        if self.config.binary_spell:
            if not self.binary_playing:
                self.binary_playing = True
                self.binary_wait = sorted(
                    self.game.get_indexed_hands(self, Creature),
                    key=lambda x: (x[1].mana_cost.count()),
                    reverse=True
                )

            remain_mana = self.game.get_remain_mana()
            self.binary_wait = list(filter(lambda x: x[1].mana_cost.count() <= remain_mana, self.binary_wait))

            if self.binary_wait.__len__() == 0:
                self.game.pass_priority()
                return

            params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
                SampleGame(
                    self,
                    Timing.PLAY_LAND,
                    self.config,
                    wait_select_spells=self.binary_wait
                ),
                self.config
            ).next_params
            spell: Optional[Tuple[int, Creature]] = None
            if "spell" in params:
                for i in self.binary_wait:
                    if i[0] == cast(List[Tuple[int, Creature]], params["spell"])[0][0]:
                        self.binary_wait.remove(i)
                        if "play" in params and params["play"]:
                            spell = i

            if "play_end" in params:
                self.game.pass_priority()
                return

            if spell is not None:
                self._play_spell(spell)
                return

            self.receive_priority()
            return

        if not self.selected_spell:
            self.selected_spell = True
            params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
                SampleGame(self, Timing.PLAY_LAND, self.config),
                self.config
            ).next_params
            if "spell" in params:
                self.selected = cast(List[Tuple[int, Creature]], params["spell"])
                self.selected = sorted(self.selected, key=lambda x: x[0], reverse=True)
            self.receive_priority()
            return

        if self.selected.__len__() > 0:
            self._play_spell(self.selected.pop(0))
        else:
            self.game.pass_priority()

    def _play_spell(self, creature: Tuple[int, Creature]):
        lands: List[Tuple[int, Land]] = self.game.get_indexed_fields(self, True, type=Land)
        land_indexes: List[Tuple[int, Land]] = require_land(creature[1], lands)
        self.game.cast_pay_cost(creature[0], get_keys_tuple_list(land_indexes))

    def declare_attackers_step(self) -> NoReturn:
        params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
            SampleGame(self, Timing.AFTER_START, self.config),
            self.config
        ).next_params
        if "attacker" in params:
            self.game.declare_attackers(cast(List[int], params["attacker"]))
        else:
            self.game.declare_attackers([])

    def declare_blockers_step(self, attackers: List[int]) -> NoReturn:
        if self.game.tmp_attacker.__len__() == 0:
            self.game.combat_damage()
            return
        params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
            SampleGame(self, Timing.SELECT_ATTACKER, self.config),
            self.config
        ).next_params
        if "blocker" in params:
            blockers: List[List[int]] = cast(List[List[int]], params["blocker"])
            for i in range(blockers.__len__()):
                self.game.declare_blokers(i, blockers[i])
        self.game.combat_damage()

    def combat_damage(self, result: Dict) -> NoReturn:
        pass

    def ending_the_game(self, win: bool) -> NoReturn:
        pass
