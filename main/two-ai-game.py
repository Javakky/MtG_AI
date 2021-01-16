import sys
from typing import NoReturn

from ai.montecalro.mcts_ai import MCTS_AI
from ai.montecalro.mtg_config import MtGConfigBuilder
from ai.reduced import Reduced
from games.game import Game


def main() -> NoReturn:
    sys.setrecursionlimit(10 ** 9)
    game: Game = Game()
    user1 = Reduced(game, "ai_1")
    user2 = MCTS_AI(game, "ai_2", MtGConfigBuilder().set_dominate_pruning(True).build())
    game.starting_the_game()
    return game.winner.name, game.reason


if __name__ == '__main__':
    result = []
    for j in range(10):
        winner = {"ai_1": 0, "ai_2": 0}
        reason = {"LO": 0, "DAMAGE": 0}
        for i in range(1):
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
