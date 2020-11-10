from typing import List, Dict

from client.console_user import ConsoleUser, print_cards
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.card_type import CardType
from games.game import Game


class Expert(ConsoleUser):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)

    def get_deck(self) -> List[Card]:
        return get_sample_deck()

    def choose_play_first(self):
        self.game.choose_play_first(self, True)

    def draw_starting_hand(self, hands: List[Card]):
        print("【" + self.name + "】の初期手札 " + str(len(hands)) + "枚：")
        print_cards(hands)
        print()

    def chosen_play_first(self, play_first: bool):
        pass

    def upkeep_step(self):
        pass

    def draw_step(self, card: Card):
        self.print_hand()
        self.game.finish_main_phase()

    def combat_damage(self, result: Dict):
        pass

    def ending_the_game(self, win: bool):
        pass

    def receive_priority(self):
        hands: List[Card] = self.game.get_hands(self)
        if not self.game.played_land():
            for i in range(hands.__len__()):
                if hands[i].has_type(CardType.LAND):
                    self.game.play_land(i)
                    print("【" + self.name + "】が土地をプレイしました：")
                    self.print_field()
                    break

    def declare_attackers_step(self):
        self.game.declare_attackers([])

    def declare_blockers_step(self, attackers: List[int]):
        pass

    def assign_damage(self, attacker: int, blockers: List[int]):
        pass
