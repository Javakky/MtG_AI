import unittest
from typing import NoReturn
from unittest import TestCase

from games.mana.color import Color
from games.mana.mana import Mana


class ManaTest(TestCase):

    def test_contains(self) -> NoReturn:
        self.assertEqual(
            False,
            Mana([Color.BLUE, 2]) in Mana(num=2)
        )
        self.assertEqual(
            False,
            Mana([Color.BLUE, 2]) in Mana(num=3)
        )
        self.assertEqual(
            True,
            Mana([Color.BLUE, 2]) in Mana([Color.BLUE, Color.BLACK, Color.RED])
        )


if __name__ == "__main__":
    unittest.main()
