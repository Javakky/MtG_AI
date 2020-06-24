from abc import ABCMeta, abstractmethod


class Card(metaclass=ABCMeta):
    def __init__(self):
        name: str

    @abstractmethod
    def type(self):
        raise NotImplementedError
