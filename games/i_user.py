from abc import *
from typing import List, Dict, TYPE_CHECKING, NoReturn, Tuple, Optional

from games.cards.card import Card
from games.cards.creature import Creature

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
    def choose_play_first(self) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def draw_starting_hand(self, hands: List[Card]) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def chosen_play_first(self, play_first: bool) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def upkeep_step(self) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def draw_step(self, card: Card) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def receive_priority(self) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def declare_attackers_step(self, P_A: Optional[List[Tuple[int, Creature]]] = None, A: Optional[List[Tuple[int, Creature]]] = None) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def declare_blockers_step(self, attackers: List[int]) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def combat_damage(self, result: Dict) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def assign_damage(self, attacker: int, blockers: List[int]) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def ending_the_game(self, win: bool) -> NoReturn:
        raise NotImplementedError
