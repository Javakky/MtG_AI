from abc import *
from typing import List

from games.cards.card import Card
from games.game import Game
from games.i_user import IUser


def print_cards(cards: List[Card]):
    for card in cards:
        print("\t" + card.__str__())


class ConsoleUser(IUser, metaclass=ABCMeta):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)

    def print_hand(self):
        print("【" + self.name + "】の手札：")
        print_cards(self.game.get_hands(self))
        print()

    def print_field(self, myself: bool = True):
        print("【" + (self.name if myself else "相手") + "】の戦場：")
        if myself:
            print_cards(self.game.get_fields(self))
        else:
            print_cards(self.game.get_fields(self.game.non_self_users(self)[0]))
        print()
