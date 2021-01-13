import copy
from itertools import combinations_with_replacement
from math import floor
from typing import List, Tuple, Optional, Iterable, Dict

from ai.ai import require_land, all_playable_creatures
from ai.montecalro.sample_player import SamplePlayer
from ai.montecalro.timing import Timing
from ai.reduced import Reduced
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from games.i_user import IUser
from util.montecalro.state import State
from util.util import get_keys_tuple_list, combinations_all


class SampleGame(Game, State):
    REWARD_DISCOUNT = 0.99
    WIN_REWARD = 1
    LOSE_REWARD = 0

    def __init__(self, player: IUser, timing: Timing):
        super().__init__()
        game: Game = player.game
        self.reward: float = 0
        self.ended: bool = False
        self.turn = game.turn
        self.player: IUser = Reduced(self, "player")
        self.enemy: IUser = Reduced(self, "enemy")
        self.players[self.player] = SamplePlayer(player, True)
        self.players[self.enemy] = SamplePlayer(game.non_self_users(player)[0], False)
        self.active_user = self.player if game.active_user == player else self.enemy
        self.now: Timing = timing
        self.tmp_attacker = copy.deepcopy(game.tmp_attacker)
        self.tmp_blocker = copy.deepcopy(game.tmp_blocker)
        self.legal_action: Optional[List[SampleGame]] = None
        self.next_params: Dict[str, object] = {}
        if game.winner is not None:
            self.reason = game.reason
            self.winner = game.winner
            self.ending_the_game(game.winner)

    def is_active(self) -> bool:
        return self.active_user == self.player

    def ending_the_game(self, winner):
        self.ended = True
        self.reward = (self.WIN_REWARD if winner == self.player else self.LOSE_REWARD) \
                      * (self.REWARD_DISCOUNT ** floor(self.turn / 2))

    @property
    def value(self) -> float:
        if not self.end:
            raise NotImplementedError()
        return self.reward

    @property
    def end(self) -> bool:
        return self.ended

    def next(self, game: 'SampleGame') -> 'SampleGame':
        return SampleGame(game.player, game.now)

    def _play_spells(self, indexes: List[int]):
        for i in reversed(indexes):
            target: Creature = self.get_hand(self.active_user, i, Creature)
            self.active_player().cast_pay_cost(
                i,
                get_keys_tuple_list(require_land(
                    target,
                    self.get_indexed_fields(self.active_user, True, Land)
                ))
            )

    @property
    def legal_actions(self) -> List['SampleGame']:
        if self.legal_action is None:
            if self.now == Timing.SELECT_ATTACKER:
                creatures: List[Tuple[int, Creature]] = self.get_indexed_fields(self.non_active_users()[0],
                                                                                type=Creature)
                p_b: Iterable[Tuple[int, ...]] = combinations_with_replacement(
                    range(0, self.tmp_attacker.__len__() + 1), creatures.__len__())
                nexts: List[SampleGame] = []
                for t in p_b:
                    next: SampleGame = SampleGame(self.player, Timing.SELECT_BLOCKER)
                    B: List[List[int]] = [[] for _ in range(self.tmp_attacker.__len__())]
                    for i in range(t.__len__()):
                        if t[i] == self.tmp_attacker.__len__():
                            continue
                        B[t[i]].append(creatures[i][0])
                    for i in range(B.__len__()):
                        self.declare_blokers(i, B[i])
                    next.next_params["blockers"] = B
                    nexts.append(next)
                self.legal_action = nexts

            elif self.now == Timing.SELECT_BLOCKER:
                lands: List[Tuple[int, Land]] = self.get_indexed_hands(self.active_user, Land)
                next: SampleGame = SampleGame(self.player, Timing.PLAY_LAND)
                if lands.__len__() != 0:
                    next._play_land(lands[0][0])
                    next.next_params["land"] = lands[0][0]
                self.legal_action = [next]

            elif self.now == Timing.PLAY_LAND:
                playable: List[List[Tuple[int, Creature]]] \
                    = all_playable_creatures(
                    self.get_indexed_hands(self.active_user, Creature),
                    self.get_remain_mana().count()
                )
                nexts: List[SampleGame] = [SampleGame(self.player, Timing.PLAY_SPELL)]
                for indexes in playable:
                    next: SampleGame = SampleGame(self.player, Timing.PLAY_SPELL)
                    next._play_spells(get_keys_tuple_list(list(indexes)))
                    next.next_params["spell"] = list(indexes)
                    nexts.append(next)
                self.legal_action = nexts

            elif self.now == Timing.PLAY_SPELL:
                creatures: List[Tuple[int, Creature]] = self.get_indexed_fields(self.non_active_users()[0],
                                                                                type=Creature)
                p_a: List[List[Tuple[int, Creature]]] = combinations_all(creatures)
                nexts: List[SampleGame] = []
                for attackers in p_a:
                    next: SampleGame = SampleGame(self.player, Timing.SELECT_ATTACKER)
                    next._start_phase()
                    next._declare_attackers(get_keys_tuple_list(attackers))
                    next.next_params["attacker"] = get_keys_tuple_list(attackers)
                    nexts.append(next)
                self.legal_action = nexts

            elif self.now == Timing.AFTER_START:
                creatures: List[Tuple[int, Creature]] = self.get_indexed_fields(self.active_user, type=Creature)
                p_a: List[List[Tuple[int, Creature]]] = combinations_all(creatures)
                nexts: List[SampleGame] = []
                for attackers in p_a:
                    next: SampleGame = SampleGame(self.player, Timing.SELECT_ATTACKER)
                    next._declare_attackers(get_keys_tuple_list(attackers))
                    next.next_params["attacker"] = get_keys_tuple_list(attackers)
                    nexts.append(next)
                self.legal_action = nexts

        return self.legal_action

    def mine(self, state: 'SampleGame') -> bool:
        if self.now == Timing.AFTER_START or self.now == Timing.PLAY_LAND:
            return True
        return False

    def playout(self) -> float:
        if self.now == Timing.PLAY_LAND:
            self.active_user.receive_priority()
        elif self.now == Timing.PLAY_SPELL:
            self.pass_priority()
        elif self.now == Timing.SELECT_ATTACKER:
            self.non_active_users()[0].declare_blockers_step(self.tmp_attacker)
        elif self.now == Timing.SELECT_BLOCKER:
            self.combat_damage()
        if self.ended:
            return self.reward
        raise NotImplementedError
