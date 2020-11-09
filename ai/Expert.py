from game.Game import Game
from game.IUser import IUser


class UserClient(IUser):
    game: Game
    name: str

    def __init__(self, game: Game, name: str):
        self.game = game
        self.game.set_user(self)
        self.name = name
