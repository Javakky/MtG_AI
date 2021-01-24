from typing import List, Dict, NoReturn, cast, Tuple, Optional, TYPE_CHECKING

from ai.ai import AI, require_land

if TYPE_CHECKING:
    from ai.montecalro.mtg_config import MtGConfig, MtGConfigBuilder
from ai.montecalro.sample_game import SampleGame
from ai.montecalro.timing import Timing
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from util.montecalro.mcts import MCTS
from util.util import get_keys_tuple_list, print_cards, print_cards_of_index


class MCTS_AI(AI):

    def __init__(self, game: Game, name: str, config: 'MtGConfig'):
        super().__init__(game, name)
        self.played_land: bool = False
        self.selected_spell: bool = False
        self.selected: List[Tuple[int, Creature]] = []
        self.config: 'MtGConfig' = config
        self.mcts: MCTS = MCTS(config)
        self.binary_complete: List[Creature] = []
        self.binary_playing: bool = False
        self.binary_selecting_attacker: bool = False

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
        self.binary_selecting_attacker = False

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
                self.binary_complete = []

            remain_mana = self.game.get_remain_mana()

            target = sorted(
                self.game.get_indexed_hands(self, Creature),
                key=lambda x: (x[1].mana_cost.count()),
                reverse=True
            )
            target = list(filter(lambda x: x[1].mana_cost.count() <= remain_mana, target))
            for comp in self.binary_complete:
                for t in target:
                    if comp == t[1]:
                        target.remove(t)

            if target.__len__() == 0:
                self.game.pass_priority()
                return

            params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
                SampleGame(
                    self,
                    Timing.PLAY_LAND,
                    self.config,
                    wait_select_spells=target
                ),
                self.config
            ).next_params

            spell: Optional[Tuple[int, Creature]] = None
            if "spell" in params:
                for i in target:
                    if i[0] == cast(List[Tuple[int, Creature]], params["spell"])[0][0]:
                        if "play" in params and params["play"]:
                            spell = i
                        else:
                            self.binary_complete.append(i[1])
                        break

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

    def declare_attackers_step(self, P_A: Optional[List[Tuple[int, Creature]]] = None,
                               A: Optional[List[Tuple[int, Creature]]] = None) -> NoReturn:
        self.game.declare_attackers(self._declare_attackers_step(P_A, A))

    def _declare_attackers_step(self, P_A: Optional[List[Tuple[int, Creature]]] = None,
                                A: Optional[List[Tuple[int, Creature]]] = None) -> List[int]:
        if self.config.attacked_policy != MCTS_AI:
            from ai.montecalro.mtg_config import MtGConfig, MtGConfigBuilder
            game: SampleGame = SampleGame(self, Timing.PLAY_SPELL,
                                          config=MtGConfigBuilder()
                                          .set_player_ai(self.config.attacked_policy)
                                          .set_enemy_ai(self.config.attacked_policy)
                                          .set_interesting_order(True)
                                          .build()
                                          )
            attacker = cast(AI, game.active_user)._declare_attackers_step()
            return attacker

        if self.config.binary_attacker:

            selected: List[Tuple[int, Creature]] = []

            print("P_B")
            print_cards_of_index(self.game.get_indexed_fields(self.game.non_active_users()[0], True, type=Creature))

            target: List[Tuple[int, Creature]] = sorted(
                self.game.get_indexed_fields(self, True, Creature),
                key=lambda x: (x[1].mana_cost.count(), x[1].power),
                reverse=True
            )

            print("P_A")
            print_cards_of_index(target)

            while target.__len__() > 0:
                params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
                    SampleGame(
                        self,
                        Timing.AFTER_START,
                        self.config,
                        wait_select_attackers=target
                    ),
                    self.config
                ).next_params

                if "attacker" in params:
                    for i in target:
                        if i[0] == cast(List[Tuple[int, Creature]], params["attacker"])[0][0]:
                            if "attack" in params and params["attack"]:
                                print("select!")
                                selected.append(i)
                            else:
                                print("pass!")
                            print_cards_of_index([i])
                            target.remove(i)
                            break
            print()
            return get_keys_tuple_list(selected)

        params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
            SampleGame(self, Timing.AFTER_START, self.config),
            self.config
        ).next_params
        if "attacker" in params:
            return cast(List[int], params["attacker"])
        else:
            return []

    def _declare_blockers_step(self, attackers: List[int],
                               P_B: Optional[List[Tuple[int, Creature]]] = None,
                               b: Optional[List[Tuple[int, Tuple[int, Creature]]]] = None
                               ) -> List[List[Tuple[int, Creature]]]:
        if self.config.blocked_policy != MCTS_AI:
            from ai.montecalro.mtg_config import MtGConfig, MtGConfigBuilder
            game: SampleGame = SampleGame(self, Timing.SELECT_ATTACKER,
                                          config=MtGConfigBuilder()
                                          .set_player_ai(self.config.blocked_policy)
                                          .set_enemy_ai(self.config.blocked_policy)
                                          .set_interesting_order(True)
                                          .build()
                                          )
            blockers: List[List[Tuple[int, Creature]]] = cast(AI, game.non_active_users()[0])._declare_blockers_step(
                game.tmp_attacker)
            return blockers

        if self.config.binary_blocker:
            selected: List[List[Tuple[int, Creature]]] = [[] for _ in range(self.game.tmp_attacker.__len__())]
            target: List[Tuple[int, Creature]] = sorted(
                self.game.get_indexed_fields(self, True, Creature),
                key=lambda x: (x[1].power, x[1].mana_cost.count()),
                reverse=True
            )

            while target.__len__() > 0:
                params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
                    SampleGame(
                        self,
                        Timing.SELECTED_ATTACKER,
                        self.config,
                        wait_select_blockers=target
                    ),
                    self.config
                ).next_params

                if "blocker" in params:
                    for i in target:
                        if i[0] == cast(Tuple[int, int], params["blocker"])[1]:
                            if cast(Tuple[int, int], params["blocker"])[0] < self.game.tmp_attacker.__len__():
                                selected[cast(Tuple[int, int], params["blocker"])[0]].append(i)
                            target.remove(i)
                            break
            return selected

        if self.game.tmp_attacker.__len__() == 0:
            return []
        params: Dict[str, object] = self.mcts.determinization_monte_carlo_tree_search_next_action(
            SampleGame(self.game.active_user, Timing.SELECT_ATTACKER, self.config),
            self.config
        ).next_params
        if "blocker" in params:
            blockers: List[List[Tuple[int, Creature]]] = cast(List[List[Tuple[int, Creature]]], params["blocker"])
            return blockers
        return []

    def declare_blockers_step(self, attackers: List[int],
                              P_B: Optional[List[Tuple[int, Creature]]] = None,
                              b: Optional[List[Tuple[int, Tuple[int, Creature]]]] = None) -> NoReturn:
        blockers: List[List[Tuple[int, Creature]]] = self._declare_blockers_step(attackers)
        for i in range(blockers.__len__()):
            self.game.declare_blokers(i, get_keys_tuple_list(blockers[i]))
        self.game.combat_damage()

    def combat_damage(self, result: Dict) -> NoReturn:
        pass

    def ending_the_game(self, win: bool) -> NoReturn:
        pass
