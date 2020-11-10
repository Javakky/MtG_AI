from abc import *
from typing import List, Dict

from game.card.Card import Card


class IUser(metaclass=ABCMeta):

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
    def recieve_priority(self):
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
