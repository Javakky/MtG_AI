from abc import ABCMeta

from game.card.Card import Card


class Permanent(Card, metaclass=ABCMeta):

    def __init__(self, name: str):
        super().__init__(name)
        self.untapped: bool = True

    def tap(self):
        self.untapped = False

    def untap(self):
        self.untapped = True
