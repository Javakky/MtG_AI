from itertools import combinations
from typing import TypeVar, Type, List, Tuple, Union, Dict, NoReturn, Iterator, Callable, Optional

from games.cards.card import Card

T = TypeVar('T', bound=object)
DEBUG = False


def assert_instanceof(__o: object, __t: Type[T]) -> NoReturn:
    if not isinstance(__o, __t):
        raise TypeError("不正な型: [要求された型 => " + __t.__name__ + ", 渡された型 => " + __o.__class__.__name__ + "]")


def flatten(list: List[Union[T, List[T]]]) -> List[T]:
    result: List[T] = []
    for element in list:
        if isinstance(element, List):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result


def debug_print(str: Union[str, Union[Exception, Dict[str, object]]] = "") -> NoReturn:
    if DEBUG:
        print(str)


def get_keys_tuple_list(list: List[Tuple[T, object]]) -> List[T]:
    return [tpl[0] for tpl in list]


def get_values_tuple_list(list: List[Tuple[object, T]]) -> List[T]:
    return [tpl[1] for tpl in list]


def index_with_default(l, x, default=False):
    if x in l:
        return l.index(x)
    else:
        return default


def print_cards(cards: List[Card]) -> NoReturn:
    for card in cards:
        print("\t" + card.__str__())


def print_cards_of_index(tuples: List[Tuple[int, Card]]) -> NoReturn:
    for t in tuples:
        print("\t(" + str(t[0]) + ", " + t[1].__str__() + ")")


def debug_print_cards(cards: List[Card]) -> NoReturn:
    if DEBUG:
        print_cards(cards)


def debug_print_cards_of_index(tuples: List[Tuple[int, Card]]) -> NoReturn:
    if DEBUG:
        print_cards_of_index(tuples)


def combinations_all(
        target: List[T],
        start: int = 0,
        filter: Optional[Callable[[Tuple[T, ...]], bool]] = None
) -> List[List[T]]:
    result: List[List[T]] = []
    for i in reversed(range(start, target.__len__() + 1)):
        comb: Iterator[Tuple[T, ...]] = combinations(target, i)
        for c in comb:
            if (filter is None) or filter(c):
                result.append(list(c))
    return result
