from abc import *
from typing import NoReturn

from games.game import Game
from games.i_user import IUser
from util.util import DEBUG, print_cards


class ConsoleUser(IUser, metaclass=ABCMeta):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)

    def print_hand(self) -> NoReturn:
        print("【" + self.name + "】の手札：")
        print_cards(self.game.get_hands(self))
        print()

    def debug_print_hand(self) -> NoReturn:
        if DEBUG:
            self.print_hand()

    def print_field(self, myself: bool = True) -> NoReturn:
        print("【" + (self.name if myself else "相手") + "】の戦場：")
        if myself:
            print_cards(self.game.get_fields(self))
        else:
            print_cards(self.game.get_fields(self.game.non_self_users(self)[0]))
        print()

    def debug_print_field(self, myself: bool = True) -> NoReturn:
        if DEBUG:
            self.print_field(myself)
