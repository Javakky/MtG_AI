from random import choice
from typing import Dict, List, Type, TypeVar

from game.IUser import IUser
from game.Player import Player
from game.card.Card import Card
from game.card.Creature import Creature
from game.card.Permanent import Permanent
from util.Exception import IllegalDamagePointsException


class Game:
    P = TypeVar('P', bound=Permanent)

    def __init__(self):
        self.players: Dict[IUser, Player] = {}
        self.play_first: IUser
        self.active_user: IUser
        self.tmp_attacker: List[int]
        self.tmp_blocker: Dict[int, List[int]]
        self.turn: int = 0

    def set_user(self, user: IUser):
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

    def non_self_users(self, self1: IUser) -> List[IUser]:
        users: List[IUser] = []
        for k in self.players.keys():
            if k != self1:
                users.append(k)
        if len(users) == 0:
            raise Exception
        return users

    def non_active_users(self) -> List[IUser]:
        return self.other_users(self.active_user)

    def other_users(self, user) -> List[IUser]:
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

    def choose_play_first(self, user: IUser, play_first: bool):
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
        self.active_user.declare_attackers_step()

    def untap_step(self):
        self.active_player().untap_all()

    def draw_step(self):
        card: Card = self.active_player().draw()
        if not card:
            self.ending_the_game(self.non_active_users()[0])
        self.active_user.draw_step(card)

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
        attacker = self.active_player().get_field(self.tmp_attacker[0], Creature)
        blockers = self.non_active_player()[0].get_fields(self.tmp_blocker[self.tmp_attacker[0]], Creature)
        result: Dict = {"damage": 0, "destroy": {"attacker": None, "blocker": []}}

        if len(blockers) < 1:
            result["damage"] = result["damage"] + attacker.power
            if self.active_player().damage(attacker.power) < 1:
                self.ending_the_game(self.active_user)
                return
        elif len(blockers) == 1:
            if attacker.power >= blockers[0].toughness:
                result["destroy"]["blocker"].append(
                    self.non_active_player()[0].destroy(blockers[0], Creature)
                )
            if attacker.toughness <= blockers[0].power:
                result["destroy"]["attacker"] = \
                    self.active_player().destroy(attacker, Creature)
        else:
            self.active_user.assign_damage(self.tmp_attacker[0], self.tmp_blocker[self.tmp_attacker[0]])
            return

        self.tmp_attacker.pop(0)
        self.active_user.combat_damage(result)

        if len(self.tmp_attacker) > 0:
            self.combat_damage()
        else:
            self.main_phase()

    def assign_damage(self, attacker_index: int, blocker_indexes: List[int], damages: List[int]):
        attacker = self.active_player().get_field(attacker_index, Creature)
        result: Dict = {"damage": 0, "destroy": {"attacker": None, "blocker": []}}

        if sum(damages) > attacker.power:
            raise IllegalDamagePointsException("割り振るダメージの合計が攻撃クリーチャーのパワーを上回っています")
        if len(blocker_indexes) != len(damages):
            raise KeyError("ブロッカーの要素数とダメージの要素数が一致しません")

        combat_damage = 0
        for i in range(len(damages)):
            blocker = self.non_active_player()[0].get_field(blocker_indexes[i], Creature)
            combat_damage = combat_damage + blocker.power
            if blocker.toughness <= damages[i]:
                result["destroy"]["blocker"].append(
                    self.non_active_player()[0].destroy(blocker_indexes[i], Creature).__str__()
                )

        if attacker.toughness <= combat_damage:
            result["destroy"]["attacker"] = \
                self.active_player().destroy(attacker_index, Creature).__str__()

        self.tmp_attacker.pop(0)
        self.active_user.combat_damage(result)

        if len(self.tmp_attacker) > 0:
            self.combat_damage()
        else:
            self.main_phase()

    def main_phase(self):
        self.active_user.recieve_priority()

    def play_land(self, index: int):
        self.active_player().play_land(index)
        self.active_user.recieve_priority()

    def cast_pay_cost(self, spell_index: int, mana_indexes: List[int]):
        self.active_player().cast_pay_cost(spell_index, mana_indexes)
        self.active_user.recieve_priority()

    def pass_priority(self):
        self.ending_phase()

    def ending_phase(self):
        self.active_user = self.non_active_users()[0]
        self.start_phase()

    def ending_the_game(self, winner: IUser):
        winner.ending_the_game(True)
        for user in self.other_users(winner):
            user.ending_the_game(False)

    def get_hands(self, user: IUser) -> List[Card]:
        return self.players[user].hand.cards

    def get_hand(self, user: IUser, index: int, type: Type[P] = Permanent) -> P:
        return self.players[user].get_hand(index, type)

    def get_field(self, user: IUser, index: int, type: Type[P] = Permanent) -> P:
        return self.players[user].get_field(index, type)

    def get_fields(self, user: IUser, type: Type[P] = Permanent) -> List[P]:
        return self.players[user].field.get_cards(type)
