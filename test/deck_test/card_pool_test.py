import unittest
from typing import cast
from unittest import TestCase

from deck.card_pool import CARD_POOL
from games.cards.creature import Creature
from games.mana.color import Color


class CardPoolTest(TestCase):
    def test_generate_test_creature(self):
        name: str = "1/2(3)"
        creature: Creature = cast(Creature, CARD_POOL.get_card(name))
        self.assertEqual(Creature, creature.__class__)
        self.assertEqual(name, creature.name)
        self.assertEqual(1, creature.power)
        self.assertEqual(2, creature.toughness)
        self.assertEqual(3, creature.mana_cost.count(Color.COLORLESS))


if __name__ == "__main__":
    unittest.main()
