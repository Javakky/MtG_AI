from typing import List, Type, TypeVar, Union

from games.cards.mana_base import ManaBase
from games.cards.permanent import Permanent
from games.mana.mana import Mana
from util.util import assert_instanceof


class Battlefield:
    P = TypeVar('P', bound=Permanent)

    def __init__(self):
        self.permanents: List[Permanent] = []

    def append(self, permanent: Permanent):
        self.permanents.append(permanent)

    def tap(self, index: int, type: Type[P] = Permanent):
        assert_instanceof(self.permanents[index], type)
        self.permanents[index].tap()

    def untap(self, index: int, type: Type[P] = Permanent):
        assert_instanceof(self.permanents[index], type)
        self.permanents[index].untap()

    def untap_all(self):
        for i in range(len(self.permanents)):
            self.untap(i)

    def get(self, index: Union[int, List[int]], type: Type[P] = Permanent) -> Union[P, List[P]]:
        if isinstance(index, list):
            result = []
            for i in index:
                assert_instanceof(self.permanents[i], type)
                result.append(self.permanents[i])
            return result

        assert_instanceof(self.permanents[index], type)
        return self.permanents[index]

    def is_untapped(self, index: int, type: Type[P] = Permanent) -> bool:
        assert_instanceof(self.permanents[index], type)
        return self.permanents[index].untapped

    def pop(self, index, type: Type[P] = Permanent) -> P:
        assert_instanceof(self.permanents[index], type)
        return self.permanents.pop(index)

    def get_cards(self, untapped: bool = None, type: Type[P] = Permanent) -> List[P]:
        result: List[Permanent] = []
        if type == Permanent:
            result = self.permanents
        else:
            for card in self.permanents:
                if isinstance(card, type):
                    result.append(card)
        if untapped is not None:
            tmp: List[P] = []
            for c in result:
                if c.untapped == untapped:
                    tmp.append(c)
            result = tmp
        return result

    def get_remain_mana(self) -> Mana:
        mana: Mana = Mana()
        for permanent in self.get_cards(type=ManaBase):
            if isinstance(permanent, ManaBase) and permanent.untapped:
                mana += permanent.mana
        return mana
