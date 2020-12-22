import sys

from ai.expert import Expert
from ai.reduced import Reduced
from games.game import Game
from util.log import write


def main():
    sys.setrecursionlimit(10 ** 9)
    game: Game = Game()
    user1 = Expert(game, "ai_1")
    user2 = Reduced(game, "ai_2")
    game.starting_the_game()
    return game.winner, game.reason


if __name__ == '__main__':
    winner = {"ai_1": 0, "ai_2": 0}
    reason = {"LO": 0, "DAMAGE": 0}
    result = []
    for j in range(10):
        for i in range(10):
            tpl = main()
            winner[tpl[0]] += 1
            reason[tpl[1]] += 1
            if i % 1000 == 0: print(i)
        message: str = "ai_1：" + str(winner["ai_1"]) + "\n" + "ai_2：" \
                       + str(winner["ai_2"]) + "\n" \
                       + "LO：" + str(reason["LO"]) + "\n" \
                       + "DAMAGE：" + str(reason["DAMAGE"])
        result.append(winner["ai_1"] / (winner["ai_1"] + winner["ai_2"]) * 100)
        write("", message, "exp_red_game\\")
    message: str = ""
    for i in result:
        message += str(i) + "%" + "\n"
    write("exp_red_result", message)
