from typing import List, Dict

from ai.ai import AI
from ai.montecalro.sample_game import SampleGame
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.game import Game


class PA(AI):

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
        self.game.finish_main_phase()

    def receive_priority(self):
        game: SampleGame = SampleGame(self)
        game.pass_priority()
        # print("reward: " + str(game.reward))
        self.game.pass_priority()

    def declare_attackers_step(self):
        self.game.declare_attackers([])

    def declare_blockers_step(self, attackers: List[int]):
        for i in range(len(attackers)):
            self.game.declare_blokers(i, [])
        self.game.combat_damage()

    def combat_damage(self, result: Dict):
        pass

    def ending_the_game(self, win: bool):
        pass
