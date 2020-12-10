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

    def __init__(self, symbols: List[Color] = None, num: int = 0):
        if symbols is None:
            symbols = []
        self.symbols: List[Color] = symbols
        self.counts: Dict[Color, int] = {}
        self.count_all: Optional[int] = None
        self.symbols.extend([Color.COLORLESS for i in range(num)])

    def __add__(self, manas: object) -> 'Mana':
        if isinstance(manas, Mana):
            return Mana(self.symbols + manas.symbols)
        if isinstance(manas, List):
            tmp: List[Color] = self.symbols
            for m in manas:
                tmp += m.symbols
            return Mana(tmp)
        else:
            raise TypeError("Manaではない型との演算に+は利用できません: " + manas.__class__.__name__)

    def count(self, color: Color = None):
        if color is not None:
            if color not in self.symbols:
                return 0
            if color not in self.counts or self.counts[color] is None:
                self.counts[color] = self.symbols.count(color)
            return self.counts[color]
        else:
            if self.count_all is None:
                self.count_all = len(self.symbols)
            return self.count_all

    def __contains__(self, mana) -> bool:
        colorless: int = 0
        for color in Color:
            if color != Color.COLORLESS:
                c = self.count(color) - mana.count(color)
                if c < 0:
                    return False
                colorless += c
        if self.count(Color.COLORLESS) + colorless - mana.count(Color.COLORLESS) < 0:
            return False
        return True

    def clone(self) -> 'Mana':
        return Mana(self.symbols)
