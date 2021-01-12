from typing import NoReturn

from client.user_client import UserClient
from games.game import Game


def main() -> NoReturn:
    game: Game = Game()
    print("一人目のユーザー名を入力してください")
    user1 = UserClient(game, input())
    print("二人目のユーザー名を入力してください")
    user2 = UserClient(game, input())
    game.starting_the_game()


if __name__ == '__main__':
    main()
