from typing import List, Dict

from client.console_user import ConsoleUser, print_cards
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.card_type import CardType
from games.cards.creature import Creature
from games.game import Game


class Expert(ConsoleUser):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)

    def get_deck(self) -> List[Card]:
        return get_sample_deck()

    def choose_play_first(self):
        self.game.choose_play_first(self, True)

    def draw_starting_hand(self, hands: List[Card]):
        pass

    def chosen_play_first(self, play_first: bool):
        pass

    def upkeep_step(self):
        pass

    def draw_step(self, card: Card):
        self.print_hand()

    def combat_damage(self, result: Dict):
        pass

    def ending_the_game(self, win: bool):
        pass

    def receive_priority(self):
        hands: List[Card] = self.game.get_hands(self)
        for i in range(hands.__len__()):
            if hands[i].has_type(CardType.LAND):
                hands.pop(i)
                self.game.play_land(i)
                print("【" + self.name + "】が土地をプレイしました：")
                self.print_field()
                print()
                break
        hands = self.game.get_hands(self, Creature)
        print(print_cards(hands))

    def declare_attackers_step(self):
        pass

    def declare_blockers_step(self, attackers: List[int]):
        pass

    def assign_damage(self, attacker: int, blockers: List[int]):
        pass
