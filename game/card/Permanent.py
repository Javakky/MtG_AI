from game.card.Card import Card


class Permanent(Card):
    untapped: bool = True

    def tap(self):
        self.untapped = False

    def untap(self):
        self.untapped = True
