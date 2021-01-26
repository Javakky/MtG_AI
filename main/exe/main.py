import json
import random
import sys
import time
from typing import Tuple, Type, TypeVar, List

from ai.ai import AI
from ai.expert import Expert
from ai.montecalro.mcts_ai import MCTS_AI
from ai.montecalro.mtg_config import MtGConfigBuilder, MtGConfig
from ai.random import RandomPlayer
from ai.reduced import Reduced
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.game import Game
from util.log import write

T = TypeVar("T", bound=AI)


def main(opponent: Type[T], player_config: MtGConfig, opponent_config: MtGConfig, order: Tuple[List[Card], List[Card]],
         first: bool):
    sys.setrecursionlimit(10 ** 9)
    game: Game = Game()
    user1 = MCTS_AI(game, "ai_1", player_config)
    if opponent == MCTS_AI:
        user2 = MCTS_AI(game, "ai_2", opponent_config)
    else:
        user2 = opponent(game, "ai_2")
    game.set_order(user1, order[0])
    game.set_order(user2, order[1])
    game.starting_the_game(user1 if first else user2)
    return game.winner.name, game.reason


AI_TYPE = ["Expert", "Reduced", "Random", "MCTS"]


def get_ai_class(class_name: str) -> Type[T]:
    if class_name == "Expert":
        return Expert
    if class_name == "Reduced":
        return Reduced
    if class_name == "Random":
        return RandomPlayer
    if class_name == "MCTS":
        return MCTS_AI
    raise Exception("存在しないAIタイプです")


def getConfig() -> Tuple[Type[T], MtGConfig, MtGConfig]:
    index: int = 1
    player_conf: MtGConfigBuilder = MtGConfigBuilder()
    opponent_conf: MtGConfigBuilder = MtGConfigBuilder()
    opponent: Type[T] = Expert
    while index < len(sys.argv):
        if sys.argv[index] == "--opponent":
            index += 1
            opponent = get_ai_class(sys.argv[index])
        elif sys.argv[index] == "--discount":
            index += 1
            player_conf.set_discount(float(sys.argv[index]))
        elif sys.argv[index] == "--win-reward":
            index += 1
            player_conf.set_win_reward(int(sys.argv[index]))
        elif sys.argv[index] == "--lose-reward":
            index += 1
            player_conf.set_lose_reward(int(sys.argv[index]))
        elif sys.argv[index] == "--no-prune":
            player_conf.set_play_land(False)
        elif sys.argv[index] == "--dominate-pruning":
            player_conf.set_dominate_pruning(True)
        elif sys.argv[index] == "--binary-spell":
            player_conf.set_binary_spell(True)
        elif sys.argv[index] == "--interesting-order":
            if index + 1 < len(sys.argv) and not sys.argv[index + 1].startswith("--"):
                index += 1
                player_conf.set_interesting_order(True, int(sys.argv[index]))
            player_conf.set_interesting_order(True)
        elif sys.argv[index] == "--player-ai":
            index += 1
            player_conf.set_player_ai(get_ai_class(sys.argv[index]))
        elif sys.argv[index] == "--opponent-ai":
            index += 1
            player_conf.set_enemy_ai(get_ai_class(sys.argv[index]))
        elif sys.argv[index] == "--expand":
            index += 1
            player_conf.set_expand(int(sys.argv[index]))
        elif sys.argv[index] == "--utc-c":
            index += 1
            player_conf.set_utc_c(float(sys.argv[index]))
        elif sys.argv[index] == "--determinizations":
            index += 1
            player_conf.set_determinizations(int(sys.argv[index]))
        elif sys.argv[index] == "--simulations":
            index += 1
            player_conf.set_simulations(int(sys.argv[index]))
        elif sys.argv[index] == "--opponent-discount":
            index += 1
            opponent_conf.set_discount(float(sys.argv[index]))
        elif sys.argv[index] == "--opponent-win-reward":
            index += 1
            opponent_conf.set_win_reward(int(sys.argv[index]))
        elif sys.argv[index] == "--opponent-lose-reward":
            index += 1
            opponent_conf.set_lose_reward(int(sys.argv[index]))
        elif sys.argv[index] == "--opponent-no-prune":
            opponent_conf.set_play_land(False)
        elif sys.argv[index] == "--opponent-dominate-pruning":
            opponent_conf.set_dominate_pruning(True)
        elif sys.argv[index] == "--opponent-binary-spell":
            opponent_conf.set_binary_spell(True)
        elif sys.argv[index] == "--opponent-interesting-order":
            if index + 1 < len(sys.argv) and not sys.argv[index + 1].startswith("--"):
                index += 1
                opponent_conf.set_interesting_order(True, int(sys.argv[index]))
            opponent_conf.set_interesting_order(True)
        elif sys.argv[index] == "--opponent-player-ai":
            index += 1
            opponent_conf.set_player_ai(get_ai_class(sys.argv[index]))
        elif sys.argv[index] == "--opponent-opponent-ai":
            index += 1
            opponent_conf.set_enemy_ai(get_ai_class(sys.argv[index]))
        elif sys.argv[index] == "--opponent-expand":
            index += 1
            opponent_conf.set_expand(int(sys.argv[index]))
        elif sys.argv[index] == "--opponent-utc-c":
            index += 1
            opponent_conf.set_utc_c(float(sys.argv[index]))
        elif sys.argv[index] == "--opponent-determinizations":
            index += 1
            opponent_conf.set_determinizations(int(sys.argv[index]))
        elif sys.argv[index] == "--opponent-simulations":
            index += 1
            opponent_conf.set_simulations(int(sys.argv[index]))
        elif sys.argv[index] == "--binary-attacker":
            player_conf.set_binary_attacker(True)
        elif sys.argv[index] == "--opponent-binary-attacker":
            opponent_conf.set_binary_attacker(True)
        elif sys.argv[index] == "--binary-blocker":
            player_conf.set_binary_blocker(True)
        elif sys.argv[index] == "--opponent-binary-blocker":
            opponent_conf.set_binary_blocker(True)
        elif sys.argv[index] == "--attacked-policy":
            index += 1
            player_conf.set_attacked_policy(get_ai_class(sys.argv[index]))
        elif sys.argv[index] == "--blocked-policy":
            index += 1
            player_conf.set_blocked_policy(get_ai_class(sys.argv[index]))
        elif sys.argv[index] == "--opponent-attacked-policy":
            index += 1
            opponent_conf.set_attacked_policy(get_ai_class(sys.argv[index]))
        elif sys.argv[index] == "--opponent-blocked-policy":
            index += 1
            opponent_conf.set_blocked_policy(get_ai_class(sys.argv[index]))
        else:
            raise Exception("存在しないオプションです")
        index += 1

    return opponent, player_conf.build(), opponent_conf.build()


if __name__ == '__main__':
    (opponent, player_config, opponent_config) = getConfig()
    msg = opponent.__name__ + "\n" + json.dumps(vars(player_config), default=lambda x: x.__name__) + "\n" + json.dumps(
        vars(opponent_config), default=lambda x: x.__name__)
    write("config_", msg, "")
    result = []
    for j in range(1000):
        seed = time.time()
        random.seed(seed)
        winner = {"ai_1": 0, "ai_2": 0}
        reason = {"LO": 0, "DAMAGE": 0}
        A = get_sample_deck()
        B = get_sample_deck()
        random.shuffle(A)
        random.shuffle(B)
        for i in range(4):
            tpl = main(opponent, player_config, opponent_config,
                       (A if i < 2 else B, B if i < 2 else A),
                       i % 2 == 0
                       )
            print(str(i))
            winner[tpl[0]] += 1
            reason[tpl[1]] += 1
        message: str = str(winner["ai_1"]) + "," \
                       + str(winner["ai_2"]) + "\n" \
                       + str(reason["LO"]) + "," \
                       + str(reason["DAMAGE"]) + "\n" \
                       + str(seed) + "\n"
        result.append(winner["ai_1"] / (winner["ai_1"] + winner["ai_2"]) * 100)
        write("", message, "")
        print(str(j))
    message: str = ""
    for i in result:
        message += str(i) + "\n"
    write("result_", message)
