from util.montecalro.config import ConfigBuilder, Config


class MtGConfig(Config):
    def __init__(self, builder: 'MtGConfigBuilder'):
        super().__init__(builder)
        self.discount: float = builder.discount
        self.win_reward: int = builder.win_reward
        self.lose_reward: int = builder.lose_reward
        self.play_land: bool = builder.play_land
        self.dominate_pruning: bool = builder.dominate_pruning
        self.binary_spell: bool = builder.binary_spell
        self.interesting_order: bool = builder.interesting_order


class MtGConfigBuilder(ConfigBuilder):
    def __init__(self):
        super().__init__()
        self.discount = 0.99
        self.win_reward = 1
        self.lose_reward = 0
        self.play_land: bool = True
        self.dominate_pruning: bool = False
        self.binary_spell: bool = False
        self.interesting_order: bool = False

    def set_discount(self, value: int) -> 'MtGConfigBuilder':
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

    def set_interesting_order(self, value: bool) -> 'MtGConfigBuilder':
        self.interesting_order = value
        return self

    def build(self) -> 'MtGConfig':
        return MtGConfig(self)
