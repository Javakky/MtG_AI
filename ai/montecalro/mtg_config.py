from util.montecalro.config import ConfigBuilder, Config


class MtGConfig(Config):
    def __init__(self, builder: 'MtGConfigBuilder'):
        super().__init__(builder)
        self.discount = builder.discount
        self.win_reward = builder.win_reward
        self.lose_reward = builder.lose_reward


class MtGConfigBuilder(ConfigBuilder):
    def __init__(self):
        super().__init__()
        self.discount = 0.99
        self.win_reward = 1
        self.lose_reward = 0

    def discount(self, value: int) -> 'MtGConfigBuilder':
        self.discount = value
        return self

    def win_reward(self, value: int) -> 'MtGConfigBuilder':
        self.win_reward = value
        return self

    def lose_reward(self, value: int) -> 'MtGConfigBuilder':
        self.lose_reward = value
        return self

    def build(self) -> 'MtGConfig':
        return MtGConfig(self)
