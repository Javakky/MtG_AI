from math import floor

from ai.montecalro.sample_player import SamplePlayer
from ai.reduced import Reduced
from games.game import Game
from games.i_user import IUser


class SampleGame(Game):
    REWARD_DISCOUNT = 0.99
    WIN_REWARD = 1
    LOSE_REWARD = 0

    def __init__(self, player: IUser):
        super().__init__()
        self.reward: float = 0
        self.player: IUser = Reduced(self, "random")
        self.enemy: IUser = Reduced(self, "ai_sample")
        self.players[self.player] = SamplePlayer(player, True)
        self.players[self.enemy] = SamplePlayer(player.game.non_self_users(self.player)[0], False)

    def ending_the_game(self, winner):
        self.reward = (self.WIN_REWARD if winner == self.player else self.LOSE_REWARD) \
                      * (self.REWARD_DISCOUNT ** floor(self.turn / 2))
