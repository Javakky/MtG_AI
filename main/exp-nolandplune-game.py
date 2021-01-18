import sys

from ai.expert import Expert
from ai.montecalro.mcts_ai import MCTS_AI
from ai.montecalro.mtg_config import MtGConfigBuilder
from games.game import Game
from util.log import write


def main():
    sys.setrecursionlimit(10 ** 9)
    game: Game = Game()
    user1 = Expert(game, "ai_1")
    user2 = MCTS_AI(game, "ai_2", MtGConfigBuilder().set_play_land(False).build())
    game.starting_the_game()
    return game.winner.name, game.reason


if __name__ == '__main__':
    result = []
    for j in range(100):
        winner = {"ai_1": 0, "ai_2": 0}
        reason = {"LO": 0, "DAMAGE": 0}
        for i in range(100):
            tpl = main()
            winner[tpl[0]] += 1
            reason[tpl[1]] += 1
            if i % 10 == 0:
                print(i)
        message: str = "ai_1：" + str(winner["ai_1"]) + "\n" + "ai_2：" \
                       + str(winner["ai_2"]) + "\n" \
                       + "LO：" + str(reason["LO"]) + "\n" \
                       + "DAMAGE：" + str(reason["DAMAGE"])
        result.append(winner["ai_1"] / (winner["ai_1"] + winner["ai_2"]) * 100)
        write("", message, "exp_nopluneland_game/")
        print(str(j))
    message: str = ""
    for i in result:
        message += str(i) + "%" + "\n"
    write("exp_nopluneland_result_", message)
