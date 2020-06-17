from typing import List

from game.mana.Color import Color


class Mana:
    symbols: List[Color] = []

    def __init__(self, symbols: List[Color]):
        self.symbols = symbols

    def extend(self, manas: List[Color]):
        self.symbols.extend(manas)

    def count(self, color: Color = None):
        if color:
            return self.symbols.count(color)
        return len(self.symbols)

    def contains(self, mana: Mana) -> bool:
        colorless: int = 0
        for color in Color:
            if color != Color.Colorless:
                c = self.count() - mana.count(color)
                if c < 0:
                    return False
                colorless += c
        if self.count(Color.Colorless) + colorless - mana.count(Color.Colorless):
            return False
        return True
