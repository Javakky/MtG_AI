from typing import List, Dict, NoReturn, Optional, Tuple

from client.console_user import ConsoleUser
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from util.Exception import IllegalManaException
from util.util import debug_print, print_cards


class UserClient(ConsoleUser):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)

    def get_deck(self) -> List[Card]:
        return get_sample_deck()

    def choose_play_first(self) -> NoReturn:
        self.game.choose_play_first(self, True)

    def chosen_play_first(self, play_first: bool) -> NoReturn:
        if play_first:
            print("【" + self.name + "】の先攻です")
            print()
        else:
            print("【" + self.name + "】は後攻です")
            print()

    def draw_starting_hand(self, hands: List[Card]) -> NoReturn:
        print("【" + self.name + "】の初期手札 " + str(len(hands)) + "枚：")
        print_cards(hands)
        print()

    def upkeep_step(self) -> NoReturn:
        print("【" + self.name + "】のターンです")
        print()

    def draw_step(self, card: Card) -> NoReturn:
        print("【" + self.name + "】のドロー：")
        print("\t" + card.__str__())

    def receive_priority(self) -> NoReturn:
        print("【" + self.name + "】が優先です：")
        print("1. カードのプレイ")
        print("2. 手札の確認")
        print("3. 自分の戦場の確認")
        print("4. 相手の戦場確認")
        print("5. 優先権の放棄")
        console_in: str = input()
        if not console_in.isdecimal():
            self.receive_priority()
        choosen: int = int(console_in)
        if not 1 <= choosen <= 5:
            print("選択された番号は存在しません")
        elif choosen == 1:
            print("プレイするカードを選択：")
            console_in: str = input()
            if not console_in.isdecimal():
                self.receive_priority()
            index: int = int(console_in)
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
                                try:
                                    self.game.cast_pay_cost(index, indexes)
                                except IllegalManaException as e:
                                    debug_print(e)
                                    self.receive_priority()
                                break
                            elif not i in indexes:
                                indexes.append(i)
                        break
                    elif choosen == 2:
                        self.print_field(True)
                    elif choosen == 3:
                        self.receive_priority()
                        break
        elif choosen == 2:
            self.print_hand()
            self.receive_priority()
        elif choosen == 3:
            self.print_field(True)
            self.receive_priority()
        elif choosen == 4:
            self.print_field(False)
            self.receive_priority()
        elif choosen == 5:
            self.game.pass_priority()

    def declare_attackers_step(self, P_A: Optional[List[Tuple[int, Creature]]] = None, A: Optional[List[Tuple[int, Creature]]] = None) -> NoReturn:
        if self.game.get_fields(self, True, Creature).__len__() < 1:
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

    def declare_blockers_step(self, attackers: List[int]) -> NoReturn:
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

    def combat_damage(self, result: Dict) -> NoReturn:
        print(result)

    def assign_damage(self, attacker: int, blockers: List[int]) -> NoReturn:
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

    def ending_the_game(self, win: bool) -> NoReturn:
        print("【" + self.name + "】は" + ("勝利" if win else "敗北") + "しました")
