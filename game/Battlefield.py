from typing import List, Type, TypeVar, Union

from game.card.Permanent import Permanent
from util.util import assert_instanceof


class Battlefield:
    P = TypeVar('P', bound=Permanent)
    permanents: List[Permanent]

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

    def get_all(self, type: Type[P] = Permanent) -> List[P]:
        if type == Permanent:
            return self.permanents

        result = []
        for permanent in self.permanents:
            if isinstance(permanent, type):
                result.append(permanent)
        return result
