from typing import List

from games.mana.color import Color


class Mana:

    def __str__(self) -> str:
        result: str = ""
        colorless: int = 0
        for symbol in self.symbols:
            if symbol == Color.COLORLESS:
                colorless += 1
            else:
                result += "(" + symbol.value + ")"
        if colorless > 0:
            result += "(" + str(colorless) + ")"
        return result

    def __init__(self, symbols=None, num: int = 0):
        if symbols is None:
            symbols = []
        self.symbols: List[Color] = symbols
        self.symbols.extend([Color.COLORLESS for i in range(num)])

    def extend(self, manas):
        self.symbols.extend(manas.symbols)

    def count(self, color: Color = None):
        if color:
            return self.symbols.count(color)
        return len(self.symbols)

    def contains(self, mana) -> bool:
        colorless: int = 0
        for color in Color:
            if color != Color.COLORLESS:
                c = self.count(color) - mana.count(color)
                if c < 0:
                    return False
                colorless += c
        if self.count(Color.COLORLESS) + colorless - mana.count(Color.COLORLESS):
            return False
        return True

    def clone(self) -> 'Mana':
        return Mana(self.symbols)
