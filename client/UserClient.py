from typing import List, Dict

from game.Game import Game
from game.IUser import IUser
from game.card.Card import Card
from game.card.Creature import Creature
from game.card.Land import Land
from game.mana.Color import Color
from game.mana.Mana import Mana


class UserClient(IUser):
    game: Game
    name: str

    def __init__(self, game: Game, name: str):
        self.game = game
        self.game.set_user(self)
        self.name = name

    def get_deck(self) -> List[Card]:
        deck: List[Card] = []
        for i in range(23):
            deck.append(Creature("真珠三叉矛の人魚", Mana([Color.Blue]), ["マーフォーク"], 1, 1))
        for i in range(17):
            deck.append(Land("島", Mana([Color.Blue])))
        return deck

    def choose_play_first(self):
        self.game.choose_play_first(self, True)

    def chosen_play_first(self, play_first: bool):
        if play_first:
            print("【" + self.name + "】の先攻です")
            print()
        else:
            print("【" + self.name + "】は後攻です")
            print()

    def draw_starting_hand(self, hands: List[Card]):
        print("【" + self.name + "】の初期手札 " + str(len(hands)) + "枚：")
        self.print_cards(hands)
        print()

    def print_hand(self):
        print("【" + self.name + "】の手札：")
        self.print_cards(self.game.get_hands(self))
        print()

    def print_field(self, myself: bool = True):
        print("【" + (self.name if myself else "相手") + "】の戦場：")
        if myself:
            self.print_cards(self.game.get_fields(self))
        else:
            self.print_cards(self.game.get_fields(self.game.non_self_users(self)[0]))
        print()

    def print_cards(self, cards: List[Card]):
        for card in cards:
            print("\t" + card.__str__())

    def upkeep_step(self):
        print("【" + self.name + "】のターンです")
        print()

    def draw_step(self, card: Card):
        print("【" + self.name + "】のドロー：")
        print("\t" + card.__str__())

    def recieve_priority(self):
        print("【" + self.name + "】が優先です：")
        print("1. カードのプレイ")
        print("2. 手札の確認")
        print("3. 優先権の放棄")
        choosen: int = int(input())
        if not 1 <= choosen <= 3:
            print("選択された番号は存在しません")
        elif choosen == 1:
            print("プレイするカードを選択：")
            index: int = int(input())
            card: Card = self.game.get_hand(self, index)
            if isinstance(card, Land):
                self.game.play_land(index)
            elif isinstance(card, Creature):
                while True:
                    print("支払うコストを選択：")
                    print("1. 土地の選択")
                    print("2. 戦場の確認")
                    print("3. 戻る")
                    choosen = int(input())
                    if not 1 <= choosen <= 3:
                        print("選択された番号は存在しません")
                    elif choosen == 1:
                        indexes: List[int] = []
                        while True:
                            print("-1. 選択を終了する")
                            print("-2. 選択を取り消す")
                            i = int(input())
                            if i < -2 or i > len(self.game.get_fields(self)) - 1:
                                print("選択された番号は存在しません")
                            elif i == -2:
                                indexes = []
                            elif i == -1:
                                self.game.cast_pay_cost(index, indexes)
                                break
                            elif not i in indexes:
                                indexes.append(i)
                        break
                    elif choosen == 2:
                        self.print_field(True)
                    elif choosen == 3:
                        self.recieve_priority()
                        break
        elif choosen == 2:
            self.print_hand()
            self.recieve_priority()
        elif choosen == 3:
            self.game.pass_priority()

    def declare_attackers_step(self):
        if len(self.game.get_fields(self, Creature)) < 1:
            self.game.declare_attackers([])
            return
        while True:
            print("【" + self.name + "】の攻撃クリーチャー選択：")
            print("1. 攻撃クリーチャー選択")
            print("2. 自分の戦場を確認")
            print("3. 相手の戦場を確認")
            choosen: int = int(input())
            if not 1 <= choosen <= 4:
                print("選択された番号は存在しません")
            elif choosen == 1:
                indexes: List[int] = []
                while True:
                    print("攻撃するクリーチャーを選択：")
                    print("-1. 選択を終了する")
                    print("-2. 選択を取り消す")
                    i = int(input())
                    if i < -2 or i > len(self.game.get_fields(self)) - 1:
                        print("選択された番号は存在しません")
                    elif i == -2:
                        indexes = []
                    elif i == -1:
                        self.game.declare_attackers(indexes)
                        break
                    elif not isinstance(self.game.get_field(self, i), Creature):
                        print("クリーチャーではありません")
                    elif not i in indexes:
                        indexes.append(i)
                break
            elif choosen == 2:
                self.print_field(True)
            elif choosen == 3:
                self.print_field(False)

    def declare_blockers_step(self, attackers: List[int]):
        while True:
            print("【" + self.name + "】の防御クリーチャー選択：")
            print("1. 防御クリーチャー選択")
            print("2. 自分の戦場を確認")
            print("3. 相手の戦場を確認")
            choosen: int = int(input())
            if not 1 <= choosen <= 4:
                print("選択された番号は存在しません")
            elif choosen == 1:
                all_indexes: List[int] = []
                for at in range(len(attackers)):
                    indexes: List[int] = []
                    while True:
                        print("防御するクリーチャーを選択：")
                        print("攻撃クリーチャー：" + self.game.get_field(self.game.active_user, attackers[at]).__str__())
                        print("-1. 選択を終了する")
                        print("-2. 選択を取り消す")
                        i = int(input())
                        if i < -2 or i > len(self.game.get_fields(self)) - 1:
                            print("選択された番号は存在しません")
                        elif i == -2:
                            indexes = []
                        elif i == -1:
                            self.game.declare_blokers(at, indexes)
                            all_indexes.extend(indexes)
                            break
                        elif not isinstance(self.game.get_field(self, i), Creature):
                            print("クリーチャーではありません")
                        elif i in all_indexes:
                            print("そのクリーチャーは既に選択されています")
                        elif not i in indexes:
                            indexes.append(i)
                self.game.combat_damage()
                break
            elif choosen == 2:
                self.print_field(True)
            elif choosen == 3:
                self.print_field(False)

    def combat_damage(self, result: Dict):
        print(result)

    def assign_damage(self, attacker: int, blockers: List[int]):
        damages: List[int] = []
        point: int = self.game.get_field(self, attacker, Creature).power
        for i in blockers:
            if point < 1:
                damages.append(0)
                continue
            while True:
                print("割り振るダメージを指定してください " + str(point) + "pt：")
                print("防御クリーチャー：" + self.game.get_field(self.game.non_active_users()[0], i).__str__())
                damage = int(input())
                if damage > point:
                    print("与えられるダメージをこえています")
                else:
                    damages.append(damage)
                    point = point - damage
                    break
        self.game.assign_damage(attacker, blockers, damages)

    def ending_the_game(self, win: bool):
        print("【" + self.name + "】は" + "勝利" if win else "敗北" + "しました")
