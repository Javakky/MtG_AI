from client.UserClient import UserClient
from game.Game import Game


def main():
    game: Game = Game()
    print("一人目のユーザー名を入力してください")
    user1 = UserClient(game, input())
    print("二人目のユーザー名を入力してください")
    user2 = UserClient(game, input())
    game.starting_the_game()


if __name__ == '__main__':
    main()
