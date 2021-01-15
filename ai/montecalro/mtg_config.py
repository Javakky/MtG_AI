from enum import Enum, auto

from util.montecalro.config import ConfigBuilder, Config


class MtGConfig(Config):
    def __init__(self, builder: 'MtGConfigBuilder'):
        super().__init__(builder)
        self.discount: float = builder.discount
        self.win_reward: int = builder.win_reward
        self.lose_reward: int = builder.lose_reward
        self.play_land: PlayLand = builder.play_land


class PlayLand(Enum):
    PLAIN = auto()
    PLUNING = auto


class MtGConfigBuilder(ConfigBuilder):
    def __init__(self):
        super().__init__()
        self.discount = 0.99
        self.win_reward = 1
        self.lose_reward = 0
        self.play_land: PlayLand = PlayLand.PLUNING

    def set_discount(self, value: int) -> 'MtGConfigBuilder':
        self.discount = value
        return self

    def set_win_reward(self, value: int) -> 'MtGConfigBuilder':
        self.win_reward = value
        return self

    def set_lose_reward(self, value: int) -> 'MtGConfigBuilder':
        self.lose_reward = value
        return self

    def set_play_land(self, value: PlayLand):
        self.play_land = value
        return self

    def build(self) -> 'MtGConfig':
        return MtGConfig(self)
