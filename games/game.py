from random import choice
from typing import Dict, List, Type, TypeVar, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from games.i_user import IUser
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.permanent import Permanent
from games.player import Player
from games.mana.mana import Mana
from util.Exception import IllegalDamagePointsException
from util.util import debug_print


class Game:
    P = TypeVar('P', bound=Permanent)
    C = TypeVar('C', bound=Card)

    def __init__(self):
        self.players: Dict[IUser, Player] = {}
        self.play_first: IUser
        self.active_user: Optional[IUser] = None
        self.tmp_attacker: List[int]
        self.tmp_blocker: Dict[int, List[int]]
        self.turn: int = 0
        self.destroy_creatures: List[Dict[str, Union[int, Dict[IUser, List[int]]]]] = []
        self.winner: str = ""
        self.reason: str = ""

    def set_user(self, user):
        self.players[user] = Player(user.get_deck())

    def active_player(self) -> Player:
        return self.players[self.active_user]

    def non_active_player(self) -> List[Player]:
        players: List[Player] = []
        for k in self.players.keys():
            if k != self.active_user:
                players.append(self.players[k])
        if len(players) == 0:
            raise Exception
        return players

    def non_self_users(self, self1) -> List:
        users: List[IUser] = []
        for k in self.players.keys():
            if k != self1:
                users.append(k)
        if len(users) == 0:
            raise Exception
        return users

    def non_active_users(self) -> List:
        return self.other_users(self.active_user)

    def other_users(self, user) -> List:
        others: List[IUser] = []
        for k in self.players.keys():
            if k != user:
                others.append(k)
        return others

    def starting_the_game(self):
        for k in self.players.keys():
            k.draw_starting_hand(self.players[k].get_hands())
        choose_player: IUser = choice(list(self.players.keys()))
        choose_player.choose_play_first()

    def choose_play_first(self, user, play_first: bool):
        if play_first:
            self.play_first = user
            self.active_user = user
        else:
            self.play_first = self.non_active_users()[0]
            self.active_user = self.non_active_users()[0]

        for k in self.players.keys():
            tmp_user: IUser = k
            if tmp_user == self.play_first:
                tmp_user.chosen_play_first(True)
            else:
                tmp_user.chosen_play_first(False)
        self.start_phase()

    def start_phase(self):
        self.turn = self.turn + 1
        self.untap_step()
        self.active_user.upkeep_step()
        if self.turn > 1:
            self.draw_step()
        else:
            self.finish_main_phase()

    def untap_step(self):
        self.active_player().untap_all()

    def draw_step(self):
        card: Card = self.active_player().draw()
        if not card:
            debug_print("山札が0枚になりました: " + str(self.active_player().get_library_count()))
            self.winner = self.non_active_users()[0].name
            self.reason = "LO"
            self.ending_the_game(self.non_active_users()[0])
        else:
            self.active_user.draw_step(card)

    def finish_main_phase(self):
        self.active_user.declare_attackers_step()

    def declare_attackers(self, indexes: List[int]):
        if len(indexes) < 1:
            self.main_phase()
            return
        self.tmp_attacker = self.active_player().declare_attackers(indexes)
        self.tmp_blocker = {}
        i: int = 0
        for attacker in self.tmp_attacker:
            self.tmp_blocker[attacker] = []
        self.non_active_users()[0].declare_blockers_step(self.tmp_attacker)

    def declare_blokers(self, attacker_index: int, blocker_indexes: List[int]):
        self.tmp_blocker[self.tmp_attacker[attacker_index]] = self.non_active_player()[0].declare_blockers(
            blocker_indexes)

    def combat_damage(self):
        if self.tmp_attacker.__len__() > 0:
            attacker = self.active_player().get_field(self.tmp_attacker[0], Creature)
            # debug_print("アタッカー：")
            # debug_print_cards([attacker])
            blockers = self.non_active_player()[0].get_fields(
                self.tmp_blocker[self.tmp_attacker[0]] if self.tmp_blocker[self.tmp_attacker[0]] is not None else [],
                Creature)
            # debug_print("ブロッカー：")
            # debug_print_cards(blockers)
            result: Dict[str, Union[int, Dict[IUser, List[int]]]] = {"damage": 0, "destroy": {self.active_user: [],
                                                                                              self.non_active_users()[
                                                                                                  0]: []}}
            if len(blockers) < 1:
                result["damage"] = result["damage"] + attacker.power
            elif len(blockers) == 1:
                if attacker.power >= blockers[0].toughness:
                    result["destroy"][self.non_active_users()[0]].append(self.tmp_blocker[self.tmp_attacker[0]][0])
                if attacker.toughness <= blockers[0].power:
                    result["destroy"][self.active_user].append(self.tmp_attacker[0])
            else:
                self.active_user.assign_damage(self.tmp_attacker[0], self.tmp_blocker[self.tmp_attacker[0]])
                return
            self.destroy_creatures.append(result)
            self.tmp_attacker.pop(0)
            self.combat_damage()
        else:
            destroy_attackers: List[int] = []
            destroy_blockers: List[int] = []
            for k in self.destroy_creatures:
                combat: Dict = {"damage": 0, "destroy": {"attacker": None, "blocker": []}}
                if k["damage"] > 0:
                    combat["damage"] += k["damage"]
                    if self.active_player().damage(k["damage"]) < 1:
                        self.active_user.combat_damage(combat)
                        debug_print("対戦相手のライフが0になりました")
                        self.ending_the_game(self.active_user)
                        self.winner = self.active_user.name
                        self.reason = "DAMAGE"
                        return
                for blocker in k["destroy"][self.non_active_users()[0]]:
                    combat["destroy"]["blocker"].append(
                        self.non_active_player()[0].get_field(blocker, Creature).__str__()
                    )
                    destroy_blockers.append(blocker)
                for attacker in k["destroy"][self.active_user]:
                    combat["destroy"]["attacker"] = \
                        self.active_player().get_field(attacker, Creature).__str__()
                    destroy_attackers.append(attacker)
                self.active_user.combat_damage(combat)
            destroy_attackers = sorted(destroy_attackers, reverse=True)
            destroy_blockers = sorted(destroy_blockers, reverse=True)
            for attacker in destroy_attackers:
                self.active_player().destroy(attacker, Creature)
            for blocker in destroy_blockers:
                self.non_active_player()[0].destroy(blocker, Creature)
            self.destroy_creatures = []
            self.main_phase()

    def assign_damage(self, attacker_index: int, blocker_indexes: List[int], damages: List[int]):
        attacker = self.active_player().get_field(attacker_index, Creature)
        result: Dict[str, Union[int, Dict[IUser, List[int]]]] = {"damage": 0, "destroy": {self.active_user: [],
                                                                                          self.non_active_users()[
                                                                                              0]: []}}
        if sum(damages) > attacker.power:
            raise IllegalDamagePointsException("割り振るダメージの合計が攻撃クリーチャーのパワーを上回っています")
        if len(blocker_indexes) != len(damages):
            raise KeyError("ブロッカーの要素数とダメージの要素数が一致しません")

        combat_damage = 0
        for i in range(len(damages)):
            blocker = self.non_active_player()[0].get_field(blocker_indexes[i], Creature)
            combat_damage = combat_damage + blocker.power
            if blocker.toughness <= damages[i]:
                result["destroy"][self.non_active_users()[0]].append(blocker_indexes[i])
        if attacker.toughness <= combat_damage:
            result["destroy"][self.active_user].append(attacker_index)

        self.destroy_creatures.append(result)
        self.tmp_attacker.pop(0)
        self.combat_damage()

    def main_phase(self):
        self.active_user.receive_priority()

    def play_land(self, index: int):
        self.active_player().play_land(index)
        self.active_user.receive_priority()

    def played_land(self):
        return self.active_player().played_land

    def cast_pay_cost(self, spell_index: int, mana_indexes: List[int]):
        self.active_player().cast_pay_cost(spell_index, mana_indexes)
        self.active_user.receive_priority()

    def pass_priority(self):
        self.ending_phase()

    def ending_phase(self):
        self.active_user = self.non_active_users()[0]
        self.start_phase()

    def ending_the_game(self, winner):
        # winner.ending_the_game(True)
        for user in self.other_users(winner):
            # user.ending_the_game(False)
            pass

    def get_hands(self, user, type: Type[C] = Card) -> List[C]:
        return self.players[user].get_hands(type)

    def get_hand(self, user, index: int, type: Type[P] = Permanent) -> P:
        return self.players[user].get_hand(index, type)

    def get_field(self, user, index: int, type: Type[P] = Permanent) -> P:
        return self.players[user].get_field(index, type)

    def get_fields(self, user, untapped: bool = None, type: Type[P] = Permanent) -> List[P]:
        return self.players[user].field.get_cards(untapped, type)

    def get_indexed_fields(self, user, untapped: bool = None, type: Type[P] = Permanent) -> List[Tuple[int, P]]:
        cards: List[Permanent] = self.get_fields(user)
        result: List[Tuple[int, P]] = []
        for i in range(cards.__len__()):
            if isinstance(cards[i], type) and \
                    (untapped is None or (cards[i].untapped == untapped)):
                result.append((i, cards[i]))
        return result

    def get_indexed_hands(self, user, type: Type[P]) -> List[Tuple[int, P]]:
        cards: List[Permanent] = self.get_hands(user)
        result: List[Tuple[int, P]] = []
        for i in range(cards.__len__()):
            if isinstance(cards[i], type):
                result.append((i, cards[i]))
        return result

    def get_remain_mana(self) -> Mana:
        return self.players[self.active_user].get_remain_mana()

    def get_life(self, user) -> int:
        return self.players[user].get_life()
