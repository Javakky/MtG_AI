from typing import List

from games.cards.card import Card
from games.cards.permanent import Permanent
from games.i_user import IUser
from games.player import Player


class SamplePlayer(Player):
    def __init__(self, user: IUser, player: bool):
        super().__init__(user.get_deck())
        self.user: bool = player
        self.life = user.game.get_life(user)
        self.init_graveyards(user.game.get_graveyards(user))
        self.init_fields(user.game.get_fields(user))
        if self.user:
            self.init_hands(user.game.get_hands(user))
        else:
            self.first_draw()

    def init_hands(self, hands: List[Card]):
        for card in hands:
            self.hand.append(self.library.pop(card.name))

    def init_graveyards(self, graveyards: List[Card]):
        for card in graveyards:
            self.graveyard.append(self.library.pop(card.name))

    def init_fields(self, fields: List[Permanent]):
        for card in fields:
            self.field.append(self.library.pop(card.name))
