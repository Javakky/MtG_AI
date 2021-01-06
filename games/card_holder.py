from abc import ABCMeta, abstractmethod


class CardHolder(metaclass=ABCMeta):
    @abstractmethod
    def append(self, card):
        raise NotImplementedError

    @abstractmethod
    def pop(self, name: str):
        raise NotImplementedError
