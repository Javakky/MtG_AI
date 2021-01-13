import sys
from typing import NoReturn

from ai.montecalro.pa import PA
from ai.reduced import Reduced
from games.game import Game


def main() -> NoReturn:
    sys.setrecursionlimit(10 ** 9)
    game: Game = Game()
    user1 = Reduced(game, "ai_1")
    user2 = PA(game, "ai_2")
    game.starting_the_game()
    return game.winner.name, game.reason


if __name__ == '__main__':
    winner = {"ai_1": 0, "ai_2": 0}
    reason = {"LO": 0, "DAMAGE": 0}
    for i in range(1):
        tpl = main()
        winner[tpl[0]] += 1
        reason[tpl[1]] += 1
        if i % 100 == 0: print(i)
    print()
    print("ai_1：" + str(winner["ai_1"]))
    print("ai_2：" + str(winner["ai_2"]))
    print("LO：" + str(reason["LO"]))
    print("DAMAGE：" + str(reason["DAMAGE"]))
