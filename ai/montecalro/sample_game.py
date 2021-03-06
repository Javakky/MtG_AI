import copy
import math
import random
from itertools import combinations_with_replacement
from math import floor
from typing import List, Tuple, Optional, Iterable, Dict, cast, TYPE_CHECKING

from ai.ai import require_land, all_playable_pairs, maximam_playable_pairs, AI
from ai.expert import Expert
from ai.montecalro import timing

if TYPE_CHECKING:
    from ai.montecalro.mtg_config import MtGConfig, MtGConfigBuilder
from ai.montecalro.sample_player import SamplePlayer
from ai.montecalro.timing import Timing
from ai.random import RandomPlayer
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from games.i_user import IUser
from util.montecalro.state import State
from util.util import get_keys_tuple_list, combinations_all


class SampleGame(Game, State):

    def __init__(self, player: IUser, timing: Timing, config: 'MtGConfig',
                 wait_select_spells: Optional[List[Tuple[int, Creature]]] = None,
                 player_fixed_ordering: Optional[List[Card]] = None,
                 enemy_fixed_ordering: Optional[List[Card]] = None,
                 was_switch: bool = False,
                 wait_select_attackers: Optional[List[Tuple[int, Creature]]] = None,
                 selected_attacker: Optional[List[Tuple[int, Creature]]] = None,
                 wait_select_blockers: Optional[List[Tuple[int, Creature]]] = None,
                 selected_blocker: Optional[List[Tuple[int, Tuple[int, Creature]]]] = None):
        super().__init__()
        if wait_select_spells is None:
            wait_select_spells = []
        if wait_select_attackers is None:
            wait_select_attackers = []
        if selected_attacker is None:
            selected_attacker = []
        if wait_select_blockers is None:
            wait_select_blockers = []
        if selected_blocker is None:
            selected_blocker = []
        game: Game = player.game
        self.reward: float = 0
        self.ended: bool = False
        self.turn = game.turn
        self.config: 'MtGConfig' = config
        self.now: Timing = timing
        self.tmp_attacker = copy.deepcopy(game.tmp_attacker)
        self.tmp_blocker = copy.deepcopy(game.tmp_blocker)
        self.legal_action: Optional[List[SampleGame]] = None
        self.next_params: Dict[str, object] = {}
        self.wait_select_spells: List[Tuple[int, Creature]] = copy.deepcopy(wait_select_spells)
        self.wait_select_attackers: List[Tuple[int, Creature]] = copy.deepcopy(wait_select_attackers)
        self.selected_attacker: List[Tuple[int, Creature]] = copy.deepcopy(selected_attacker)
        self.wait_select_blockers: List[Tuple[int, Creature]] = copy.deepcopy(wait_select_blockers)
        self.selected_blocker: List[Tuple[int, Tuple[int, Creature]]] = copy.deepcopy(selected_blocker)
        self.was_switch: bool = was_switch
        self.player: AI = self.config.player_ai(self, "player")
        self.enemy: AI = self.config.enemy_ai(self, "enemy")
        self.active_user = self.player if game.active_user == player else self.enemy
        self.players[self.player] = SamplePlayer(player, True, set_order=self.config.interesting_order)
        self.players[self.enemy] = SamplePlayer(game.non_self_users(player)[0], False,
                                                set_order=self.config.interesting_order)
        self.player_order: Optional[List[Card]] = None
        self.enemy_order: Optional[List[Card]] = None
        if self.config.interesting_order:
            if player_fixed_ordering is not None:
                self.player_order = player_fixed_ordering
                self.enemy_order = enemy_fixed_ordering
            else:
                (self.player_order, self.enemy_order) = self.get_interesting_orders()
            cast(SamplePlayer, self.players[self.player]).set_order(self.player_order)
            cast(SamplePlayer, self.players[self.enemy]).set_order(self.enemy_order)

        if game.winner is not None:
            self.reason = game.reason
            self.winner = game.winner
            self.ending_the_game(game.winner)

    def is_active(self) -> bool:
        return self.active_user == self.player

    def ending_the_game(self, winner):
        self.ended = True
        self.reward = (self.config.win_reward if winner == self.player else self.config.lose_reward) \
                      * (self.config.discount ** floor(self.turn / 2))

    @property
    def value(self) -> float:
        if not self.end:
            raise NotImplementedError()
        return self.reward

    @property
    def end(self) -> bool:
        return self.ended

    def next(self, now: Timing = None, wait_select_spells: bool = False,
             config: Optional['MtGConfig'] = None, was_swich: bool = False,
             wait_select_attackers: bool = False, selected_attacker: bool = False,
             wait_select_blockers: bool = False,
             selected_blocker: bool = False) -> 'SampleGame':
        if now is None:
            now = self.now
        if config is None:
            config = self.config
        return SampleGame(
            self.enemy if was_swich else self.player,
            now,
            config,
            self.wait_select_spells if wait_select_spells else None,
            self.player_order if was_swich else self.enemy_order,
            self.enemy_order if was_swich else self.player_order,
            was_swich,
            self.wait_select_attackers,
            self.selected_attacker,
            self.wait_select_blockers,
            self.selected_blocker
        )

    def _play_spells(self, indexes: List[int]):
        for i in reversed(sorted(indexes)):
            target: Creature = self.get_hand(self.active_user, i, Creature)
            self.active_player().cast_pay_cost(
                i,
                get_keys_tuple_list(require_land(
                    target,
                    self.get_indexed_fields(self.active_user, True, type=Land)
                ))
            )
            if self.config.binary_spell:
                waits = self.wait_select_spells
                results = []
                for i in self.get_indexed_hands(self.active_user, Land):
                    for w in waits:
                        if i[1].name == w[1].name:
                            results.append(i)
                            break
                self.wait_select_spells = results

    @property
    def legal_actions(self) -> List['SampleGame']:
        if self.legal_action is None:
            if self.now == Timing.SELECT_ATTACKER or self.now == Timing.SELECTED_ATTACKER:
                self.legal_action = self.legal_select_blocker()
            elif self.now == Timing.SELECT_BLOCKER or self.now == Timing.BEFORE_LAND:
                self.legal_action = self.legal_play_land()

            elif self.now == Timing.PLAY_LAND:
                self.legal_action = self.legal_play_spell()

            elif self.now == Timing.AFTER_START or self.now == Timing.PLAY_SPELL:
                self.legal_action = self.legal_select_attacker(self.now == Timing.AFTER_START)

        return self.legal_action

    def legal_select_blocker(self):
        creatures: List[Tuple[int, Creature]] = self.get_indexed_fields(self.non_active_users()[0],
                                                                        type=Creature)
        if self.config.binary_blocker:
            future: List[SampleGame] = []
            if self.wait_select_blockers.__len__() == 0:
                self.wait_select_blockers = sorted(
                    self.get_indexed_fields(self.non_active_users()[0], True, Creature),
                    key=lambda x: (x[1].mana_cost.count(), x[1].power),
                    reverse=True
                )
            for i in reversed(range(self.tmp_attacker.__len__() + 1)):
                next: SampleGame = self.next(
                    Timing.SELECTED_ATTACKER if self.wait_select_blockers.__len__() > 1 else Timing.SELECT_BLOCKER,
                    was_swich=self.now == Timing.SELECT_ATTACKER,
                    wait_select_blockers=True,
                    selected_blocker=True
                )
                creature: Tuple[int, Creature] = next.wait_select_blockers.pop(0)
                next.next_params["blocker"] = (i, creature[0])
                next.selected_blocker.append((i, creature))
                if next.wait_select_blockers.__len__() == 0:
                    B: List[List[int]] = [[] for _ in range(next.tmp_attacker.__len__())]
                    for tpl in next.selected_blocker:
                        if tpl[0] != next.tmp_attacker.__len__():
                            B[tpl[0]].append(tpl[1][0])
                    for j in range(B.__len__()):
                        next.declare_blokers(j, B[j])
                future.append(next)
            return future

        p_b: Iterable[Tuple[int, ...]] = combinations_with_replacement(
            range(0, self.tmp_attacker.__len__() + 1), creatures.__len__())
        nexts: List[SampleGame] = []
        for t in p_b:
            next: SampleGame = self.next(Timing.SELECT_BLOCKER, was_swich=True)
            B: List[List[Tuple[int, Creature]]] = [[] for _ in range(self.tmp_attacker.__len__())]
            for i in range(t.__len__()):
                if t[i] == self.tmp_attacker.__len__():
                    continue
                B[t[i]].append(creatures[i])
            for i in range(B.__len__()):
                next.declare_blokers(i, get_keys_tuple_list(B[i]))
            next.next_params["blocker"] = B
            nexts.append(next)
        return nexts

    def legal_play_land(self) -> List['SampleGame']:
        if self.config.play_land:
            lands: List[Tuple[int, Land]] = self.get_indexed_hands(self.active_user, Land)
            next: SampleGame = self.next(Timing.PLAY_LAND, was_swich=(self.now == Timing.SELECT_BLOCKER))
            if lands.__len__() != 0:
                next._play_land(lands[0][0])
                next.next_params["land"] = lands[0][0]
            return [next]

        lands: List[Tuple[int, Land]] = self.get_indexed_hands(self.active_user, Land)
        nexts: List[SampleGame] = [self.next(Timing.PLAY_LAND, was_swich=(self.now == Timing.SELECT_BLOCKER))]
        if lands.__len__() != 0:
            next: SampleGame = self.next(Timing.PLAY_LAND, was_swich=(self.now == Timing.SELECT_BLOCKER))
            next._play_land(lands[0][0])
            next.next_params["land"] = lands[0][0]
            nexts.append(next)
        return nexts

    def legal_play_spell(self):
        playable: List[List[Tuple[int, Creature]]] = self.get_playable_pairs()

        if self.config.binary_spell:
            if self.wait_select_spells.__len__() == 0:
                self.wait_select_spells = list(filter(
                    lambda x: x[1].mana_cost.count() <= self.get_remain_mana(),
                    sorted(
                        self.get_indexed_hands(self.active_user, Creature),
                        key=lambda x: (x[1].mana_cost.count()),
                        reverse=True
                    )
                ))
            play: SampleGame = self.next(Timing.PLAY_LAND, wait_select_spells=True)
            not_play: SampleGame = self.next(Timing.PLAY_LAND, wait_select_spells=True)
            while play.wait_select_spells.__len__() > 0:
                spell: Tuple[int, Creature] = play.wait_select_spells.pop(0)
                notp_spell: Tuple[int, Creature] = not_play.wait_select_spells.pop(0)
                for pair in playable:
                    for target in pair:
                        if spell[0] == target[0]:
                            break
                    else:
                        continue
                    break
                else:
                    continue
                play.next_params["spell"] = [spell]
                play.next_params["play"] = True
                not_play.next_params["spell"] = [notp_spell]
                play._play_spells([spell[0]])
                break
            else:
                tmp = self.next(Timing.PLAY_SPELL)
                tmp.next_params["play_end"] = True
                return [tmp]
            return [play, not_play]

        nexts: List[SampleGame] = [self.next(Timing.PLAY_SPELL)]

        for indexes in playable:
            next: SampleGame = self.next(Timing.PLAY_SPELL)
            next._play_spells(get_keys_tuple_list(indexes))
            next.next_params["spell"] = indexes
            nexts.append(next)

        return nexts

    def legal_select_attacker(self, myturn: bool) -> List['SampleGame']:
        if self.config.binary_attacker:
            if self.wait_select_attackers.__len__() == 0:
                self.wait_select_attackers = sorted(
                    self.get_indexed_fields(self.active_user, True, Creature),
                    key=lambda x: (x[1].mana_cost.count(), x[1].power),
                    reverse=True
                )
            play: SampleGame = self.next(
                Timing.AFTER_START if self.wait_select_attackers.__len__() > 1 else Timing.SELECT_ATTACKER,
                wait_select_attackers=True,
                selected_attacker=True,
                was_swich=not myturn
            )
            not_play: SampleGame = self.next(
                Timing.AFTER_START if self.wait_select_attackers.__len__() > 1 else Timing.SELECT_ATTACKER,
                wait_select_attackers=True,
                selected_attacker=True,
                was_swich=not myturn
            )
            if not myturn:
                play._start_phase()
                not_play._start_phase()
            creature: Tuple[int, Creature] = play.wait_select_attackers.pop(0)
            nota_creature: Tuple[int, Creature] = not_play.wait_select_attackers.pop(0)
            play.next_params["attacker"] = [creature]
            play.next_params["attack"] = True
            not_play.next_params["attacker"] = [nota_creature]
            play.selected_attacker.append(creature)
            if play.wait_select_attackers.__len__() == 0:
                play._declare_attackers(get_keys_tuple_list(play.selected_attacker))
            return [play, not_play]

        if myturn:
            creatures: List[Tuple[int, Creature]] = self.get_indexed_fields(self.active_user, type=Creature)
        else:
            creatures: List[Tuple[int, Creature]] = self.get_indexed_fields(
                self.non_active_users()[0],
                type=Creature
            )
        p_a: List[List[Tuple[int, Creature]]] = combinations_all(creatures)
        nexts: List[SampleGame] = []
        for attackers in p_a:
            next: SampleGame = self.next(Timing.SELECT_ATTACKER, was_swich=not myturn)
            if not myturn:
                next._start_phase()
            next._declare_attackers(get_keys_tuple_list(attackers))
            next.next_params["attacker"] = get_keys_tuple_list(attackers)
            nexts.append(next)
        return nexts

    def switched(self) -> bool:
        return self.was_switch

    def playout(self) -> float:
        if self.now == Timing.PLAY_LAND:
            self.active_user.receive_priority()
        elif self.now == Timing.PLAY_SPELL:
            self.pass_priority()
        elif self.now == Timing.AFTER_START:
            if self.config.binary_attacker:
                self.active_user.declare_attackers_step(self.wait_select_attackers, self.selected_attacker)
            else:
                self.active_user.declare_attackers_step()
        elif self.now == Timing.SELECTED_ATTACKER:
            if self.config.binary_blocker:
                self.non_active_users()[0].declare_blockers_step(self.tmp_attacker, self.wait_select_blockers,
                                                                 self.selected_blocker)
        elif self.now == Timing.SELECT_ATTACKER:
            self.non_active_users()[0].declare_blockers_step(self.tmp_attacker)
        elif self.now == Timing.SELECT_BLOCKER:
            self.combat_damage()
        if self.ended:
            return self.reward
        raise NotImplementedError

    def get_playable_pairs(self):

        if self.config.dominate_pruning:
            return maximam_playable_pairs(
                self.get_indexed_hands(self.active_user, Creature),
                self.get_remain_mana()
            )

        return all_playable_pairs(
            self.get_indexed_hands(self.active_user, Creature),
            self.get_remain_mana()
        )

    def get_interesting_orders(self) -> Tuple[List[Card], List[Card]]:
        player_ordering: List[Card] = copy.deepcopy(self.players[self.player].library.cards)
        enemy_ordering: List[Card] = copy.deepcopy(self.players[self.enemy].library.cards)
        for _ in range(math.floor(self.config.simulations * 0.05) + 1):
            random.shuffle(player_ordering)
            random.shuffle(enemy_ordering)
            (play, no_play) = self.is_interesting_by_expert_rollout_model(player_ordering, enemy_ordering)
            if play is None:
                return player_ordering, enemy_ordering
            for _ in range(self.config.find_per_once):
                tmp_play = play.next(play.now)
                tmp_no_play = no_play.next(no_play.now)
                tmp_play.playout()
                tmp_no_play.playout()
                if (tmp_play.winner == tmp_play.active_user) != (tmp_no_play.winner == tmp_no_play.active_user):
                    return player_ordering, enemy_ordering
        return player_ordering, enemy_ordering

    def is_interesting_by_expert_rollout_model(
            self, player_ordering: List[Card], enemy_ordering: List[Card]
    ) -> Tuple[Optional['SampleGame'], Optional['SampleGame']]:
        next: Timing = timing.next(self.now)
        from ai.montecalro.mtg_config import MtGConfigBuilder
        config: 'MtGConfig' = MtGConfigBuilder() \
            .set_player_ai(RandomPlayer) \
            .set_enemy_ai(RandomPlayer) \
            .set_interesting_order(True) \
            .build()
        play = SampleGame(
            self.player, next, config,
            player_fixed_ordering=player_ordering,
            enemy_fixed_ordering=enemy_ordering
        )
        no_play = SampleGame(
            self.player, next, config,
            player_fixed_ordering=player_ordering,
            enemy_fixed_ordering=enemy_ordering
        )
        game: SampleGame = play.next(next, config=MtGConfigBuilder()
                                     .set_player_ai(Expert)
                                     .set_enemy_ai(Expert)
                                     .set_interesting_order(True)
                                     .build())
        if next == Timing.PLAY_LAND:
            return None, None
        if next == Timing.PLAY_SPELL:
            spells = get_keys_tuple_list(cast(Expert, game.active_user)._play_spell())
            if spells.__len__() == 0:
                return None, None
            play._play_spells(spells)
        if next == Timing.SELECT_ATTACKER:
            if self.now == Timing.PLAY_SPELL:
                play._start_phase()
                game._start_phase()
            attacker = cast(Expert, game.active_user)._declare_attackers_step()
            if attacker.__len__() == 0:
                return None, None
            play._declare_attackers(attacker)
        if next == Timing.SELECT_BLOCKER:
            blocker: List[List[Tuple[int, Creature]]] \
                = cast(Expert, game.non_active_users()[0])._declare_blockers_step(game.tmp_attacker)
            if blocker.__len__() == 0:
                return None, None
            for i in range(blocker.__len__()):
                play.declare_blokers(i, get_keys_tuple_list(blocker[i]))
        return play, no_play
