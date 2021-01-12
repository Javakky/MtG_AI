from typing import NoReturn

from ai.expert import Expert
from client.user_client import UserClient
from games.game import Game


def main() -> NoReturn:
    game: Game = Game()
    print("ユーザー名を入力してください")
    user1 = UserClient(game, input())
    user2 = Expert(game, "ai")
    game.starting_the_game()


if __name__ == '__main__':
    main()
