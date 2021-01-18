from abc import ABCMeta, abstractmethod


class Config:
    def __init__(self, builder: 'ConfigBuilder'):
        self.expand: int = builder.expand
        self.UTC_C: float = builder.UTC_C
        self.determinizations: int = builder.determinizations
        self.simulations: int = builder.simulations


class ConfigBuilder(metaclass=ABCMeta):
    def __init__(self):
        self.expand: int = 10
        self.UTC_C: float = 1.5
        self.determinizations: int = 40
        self.simulations: int = 250

    def set_utc_c(self, value: float) -> 'ConfigBuilder':
        self.UTC_C = value
        return self

    def set_expand(self, value: int) -> 'ConfigBuilder':
        self.expand = value
        return self

    def set_determinizations(self, value: int) -> 'ConfigBuilder':
        self.determinizations = value
        return self

    def set_simulations(self, value: int) -> 'ConfigBuilder':
        self.simulations = value
        return self

    @abstractmethod
    def build(self) -> 'Config':
        raise NotImplementedError()
