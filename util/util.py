from typing import TypeVar, Type, List

T = TypeVar('T', bound=object)


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
