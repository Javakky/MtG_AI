import sys

from ai.expert import Expert
from ai.random import RandomPlayer
from ai.reduced import Reduced
from games.game import Game
from util.log import write


def main():
    sys.setrecursionlimit(10 ** 9)
    game: Game = Game()
    user1 = RandomPlayer(game, "ai_1")
    user2 = Reduced(game, "ai_2")
    game.starting_the_game()
    return game.winner.name, game.reason


if __name__ == '__main__':
    result = []
    for j in range(10000):
        winner = {"ai_1": 0, "ai_2": 0}
        reason = {"LO": 0, "DAMAGE": 0}
        for i in range(1000):
            tpl = main()
            winner[tpl[0]] += 1
            reason[tpl[1]] += 1
        message: str = "ai_1：" + str(winner["ai_1"]) + "\n" + "ai_2：" \
                       + str(winner["ai_2"]) + "\n" \
                       + "LO：" + str(reason["LO"]) + "\n" \
                       + "DAMAGE：" + str(reason["DAMAGE"])
        result.append(winner["ai_1"] / (winner["ai_1"] + winner["ai_2"]) * 100)
        write("", message, "rand_red_game_2021-01-07/")
        print(str(j))
    message: str = ""
    for i in result:
        message += str(i) + "%" + "\n"
    write("rand_red_result", message)
