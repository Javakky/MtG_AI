from typing import List, Type, TypeVar, Union, Optional, NoReturn

from games.card_holder import CardHolder
from games.cards.mana_base import ManaBase
from games.cards.permanent import Permanent
from games.mana.mana import Mana
from util.util import assert_instanceof

P = TypeVar('P', bound=Permanent)


class Battlefield(CardHolder):

    def __init__(self):
        self.permanents: List[Permanent] = []

    def pop(self, name: str) -> Optional[Permanent]:
        if name is None:
            raise NotImplementedError
        for card in self.permanents:
            if card.name == name:
                self.permanents.remove(card)
                return card
        return None

    def append(self, permanent: Permanent) -> NoReturn:
        self.permanents.append(permanent)

    def tap(self, index: int, type: Type[P] = Permanent) -> NoReturn:
        assert_instanceof(self.permanents[index], type)
        self.permanents[index].tap()

    def untap(self, index: int, type: Type[P] = Permanent) -> NoReturn:
        assert_instanceof(self.permanents[index], type)
        self.permanents[index].untap()

    def untap_all(self) -> NoReturn:
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

    def pop_index(self, index, type: Type[P] = Permanent) -> P:
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

    def get_remain_mana(self) -> int:
        mana: int = 0
        for permanent in self.get_cards(True, ManaBase):
            mana += permanent.mana.count()
        return mana
