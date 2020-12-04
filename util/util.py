from typing import TypeVar, Type, List, Tuple

T = TypeVar('T', bound=object)
DEBUG = True


def assert_instanceof(__o: object, __t: Type[T]):
    if not isinstance(__o, __t):
        raise TypeError("不正な型: [要求された型 => " + __t.__name__ + ", 渡された型 => " + __o.__class__.__name__ + "]")


def flatten(list: List[T]):
    result: List[T] = []
    for element in list:
        if isinstance(element, List):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result


def debug_print(str: str = ""):
    if DEBUG:
        print(str)


def get_keys_tuple_list(list: List[Tuple[T, object]]) -> List[T]:
    return [tpl[0] for tpl in list]


def get_values_tuple_list(list: List[Tuple[object, T]]) -> List[T]:
    return [tpl[1] for tpl in list]
