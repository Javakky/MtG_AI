from typing import List, NoReturn, Optional

from games.cards.card import Card
from games.cards.permanent import Permanent
from games.i_user import IUser
from games.player import Player


class SamplePlayer(Player):
    def __init__(self, user: IUser, player: bool):
        super().__init__(user.get_deck())
        self.user: bool = player
        self.life = user.game.get_life(user)
        self.init_fields(user.game.get_fields(user))
        self.init_graveyards(user.game.get_graveyards(user))
        if self.user:
            self.init_hands(user.game.get_hands(user))
        else:
            self.first_draw()

    def init_hands(self, hands: List[Card]) -> NoReturn:
        for card in hands:
            self.hand.append(self.library.pop(card.name))

    def init_graveyards(self, graveyards: List[Card]) -> NoReturn:
        for card in graveyards:
            self.graveyard.append(self.library.pop(card.name))

    def init_fields(self, fields: List[Permanent]) -> NoReturn:
        for card in fields:
            tmp: Permanent = self.library.pop(card.name)
            if not card.untapped:
                tmp.tap()
            self.field.append(tmp)
