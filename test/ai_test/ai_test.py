from typing import NoReturn, cast
from unittest import TestCase

from ai.ai import maximam_playable_pairs
from deck.card_pool import CARD_POOL
from games.cards.creature import Creature


class AITest(TestCase):

    def test_maximam_playable_pairs(self) -> NoReturn:
        a_1 = cast(Creature, CARD_POOL.get_card("1/1(1)"))
        b_1 = cast(Creature, CARD_POOL.get_card("2/2(2)"))
        c_1 = cast(Creature, CARD_POOL.get_card("3/3(3)"))
        a_2 = cast(Creature, CARD_POOL.get_card("1/1(1)"))
        b_2 = cast(Creature, CARD_POOL.get_card("2/2(2)"))
        c_2 = cast(Creature, CARD_POOL.get_card("3/3(3)"))
        self.assertEqual(
            [
                [(0, a_1), (1, a_2), (2, b_1), (3, b_2)],
                [(0, a_1), (1, a_2), (4, c_1)],
                [(0, a_1), (1, a_2), (5, c_2)],
                [(0, a_1), (2, b_1), (4, c_1)],
                [(0, a_1), (2, b_1), (5, c_2)],
                [(0, a_1), (3, b_2), (4, c_1)],
                [(0, a_1), (3, b_2), (5, c_2)],
                [(1, a_2), (2, b_1), (4, c_1)],
                [(1, a_2), (2, b_1), (5, c_2)],
                [(1, a_2), (3, b_2), (4, c_1)],
                [(1, a_2), (3, b_2), (5, c_2)],
                [(4, c_1), (5, c_2)]
            ],
            maximam_playable_pairs(
                [
                    (0, a_1),
                    (1, a_2),
                    (2, b_1),
                    (3, b_2),
                    (4, c_1),
                    (5, c_2),
                ], 6
            )
        )
