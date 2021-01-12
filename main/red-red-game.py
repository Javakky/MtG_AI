import sys
from typing import NoReturn

from ai.reduced import Reduced
from games.game import Game


def main() -> NoReturn:
    sys.setrecursionlimit(10 ** 9)
    game: Game = Game()
    user1 = Reduced(game, "ai_1")
    user2 = Reduced(game, "ai_2")
    game.starting_the_game()
    return game.winner.name, game.reason


if __name__ == '__main__':
    main()
