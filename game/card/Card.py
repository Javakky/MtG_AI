from abc import ABCMeta, abstractmethod


class Card(metaclass=ABCMeta):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def type(self):
        raise NotImplementedError
