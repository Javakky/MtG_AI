import sys

from ai.expert import Expert
from ai.random import RandomPlayer
from games.game import Game


def main():
    sys.setrecursionlimit(10 ** 9)
    game: Game = Game()
    user1 = Expert(game, "ai_1")
    user2 = RandomPlayer(game, "ai_2")
    game.starting_the_game()
    return game.winner, game.reason


if __name__ == '__main__':
    result = []
    for j in range(1):
        winner = {"ai_1": 0, "ai_2": 0}
        reason = {"LO": 0, "DAMAGE": 0}
        for i in range(1000):
            tpl = main()
            winner[tpl[0]] += 1
            reason[tpl[1]] += 1
            if i % 100 == 0:
                print(i)
        message: str = "ai_1：" + str(winner["ai_1"]) + "\n" + "ai_2：" \
                       + str(winner["ai_2"]) + "\n" \
                       + "LO：" + str(reason["LO"]) + "\n" \
                       + "DAMAGE：" + str(reason["DAMAGE"])
        print(message)
