from typing import Type, TypeVar, TYPE_CHECKING

from ai.ai import AI
from ai.expert import Expert

if TYPE_CHECKING:
    from ai.montecalro.mcts_ai import MCTS_AI
from ai.reduced import Reduced
from util.montecalro.config import ConfigBuilder, Config

A = TypeVar('A', bound=AI)


class MtGConfig(Config):
    def __init__(self, builder: 'MtGConfigBuilder'):
        super().__init__(builder)
        self.binary_blocker: bool = builder.binary_blocker
        self.discount: float = builder.discount
        self.win_reward: int = builder.win_reward
        self.lose_reward: int = builder.lose_reward
        self.play_land: bool = builder.play_land
        self.dominate_pruning: bool = builder.dominate_pruning
        self.binary_spell: bool = builder.binary_spell
        self.interesting_order: bool = builder.interesting_order
        self.find_per_once: int = builder.find_per_once
        self.binary_attacker: bool = builder.binary_attacker
        self.player_ai: Type[A] = builder.player_ai
        self.enemy_ai: Type[A] = builder.enemy_ai
        self.attacked_policy: Type[A] = builder.attacked_policy
        self.blocked_policy: Type[A] = builder.blocked_policy


class MtGConfigBuilder(ConfigBuilder):
    def __init__(self):
        super().__init__()
        from ai.montecalro.mcts_ai import MCTS_AI
        self.blocked_policy: Type[A] = MCTS_AI
        self.attacked_policy: Type[A] = MCTS_AI
        self.discount: float = 0.99
        self.win_reward: int = 1
        self.lose_reward: int = 0
        self.play_land: bool = True
        self.dominate_pruning: bool = False
        self.binary_spell: bool = False
        self.interesting_order: bool = False
        self.find_per_once: int = 5
        self.player_ai: Type[A] = Reduced
        self.enemy_ai: Type[A] = Reduced
        self.binary_attacker: bool = False
        self.binary_blocker: bool = False

    def set_discount(self, value: float) -> 'MtGConfigBuilder':
        self.discount = value
        return self

    def set_win_reward(self, value: int) -> 'MtGConfigBuilder':
        self.win_reward = value
        return self

    def set_lose_reward(self, value: int) -> 'MtGConfigBuilder':
        self.lose_reward = value
        return self

    def set_play_land(self, value: bool) -> 'MtGConfigBuilder':
        self.play_land = value
        return self

    def set_dominate_pruning(self, value: bool) -> 'MtGConfigBuilder':
        self.dominate_pruning = value
        return self

    def set_binary_spell(self, value: bool) -> 'MtGConfigBuilder':
        self.binary_spell = value
        return self

    def set_binary_attacker(self, value: bool) -> 'MtGConfigBuilder':
        self.binary_attacker = value
        from ai.montecalro.mcts_ai import MCTS_AI
        self.attacked_policy = MCTS_AI
        return self

    def set_binary_blocker(self, value: bool) -> 'MtGConfigBuilder':
        self.binary_blocker = value
        from ai.montecalro.mcts_ai import MCTS_AI
        self.blocked_policy = MCTS_AI
        return self

    def set_interesting_order(self, use: bool, find_count: int = 5) -> 'MtGConfigBuilder':
        self.interesting_order = use
        if use:
            self.find_per_once = find_count
        return self

    def set_player_ai(self, value: Type[A]):
        self.player_ai = value
        return self

    def set_enemy_ai(self, value: Type[A]):
        self.enemy_ai = value
        return self

    def set_attacked_policy(self, value: Type[A]):
        self.attacked_policy = value
        return self

    def set_blocked_policy(self, value: Type[A]):
        self.blocked_policy = value
        return self

    def build(self) -> 'MtGConfig':
        return MtGConfig(self)
