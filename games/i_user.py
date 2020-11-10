from abc import *
from typing import List, Dict, TYPE_CHECKING

from games.cards.card import Card

if TYPE_CHECKING:
    from games.game import Game


class IUser(metaclass=ABCMeta):

    def __init__(self, game, name: str):
        self.game: Game = game
        self.game.set_user(self)
        self.name: str = name

    @abstractmethod
    def get_deck(self) -> List[Card]:
        raise NotImplementedError

    @abstractmethod
    def choose_play_first(self):
        raise NotImplementedError

    @abstractmethod
    def draw_starting_hand(self, hands: List[Card]):
        raise NotImplementedError

    @abstractmethod
    def chosen_play_first(self, play_first: bool):
        raise NotImplementedError

    @abstractmethod
    def upkeep_step(self):
        raise NotImplementedError

    @abstractmethod
    def draw_step(self, card: Card):
        raise NotImplementedError

    @abstractmethod
    def receive_priority(self):
        raise NotImplementedError

    @abstractmethod
    def declare_attackers_step(self):
        raise NotImplementedError

    @abstractmethod
    def declare_blockers_step(self, attackers: List[int]):
        raise NotImplementedError

    @abstractmethod
    def combat_damage(self, result: Dict):
        raise NotImplementedError

    @abstractmethod
    def assign_damage(self, attacker: int, blockers: List[int]):
        raise NotImplementedError

    @abstractmethod
    def ending_the_game(self, win: bool):
        raise NotImplementedError
