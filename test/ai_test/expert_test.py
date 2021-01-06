import unittest
from typing import cast, Tuple
from unittest import TestCase

from ai.ai import find_damage_destroyable_max_cost_assign
from ai.expert import exists_one_sidedly_destroied_pair, exists_exchanged_low_cost_pair, \
    exists_exchange_high_cost_next_turn, find_one_sidedly_destroied_smaller_cost_pair, find_exchanged_low_cost_creature, \
    maximum_playable_creature_count_enough_land, count_smallest_pair_exceeds_my_life, find_exchanged_creature_pair
from deck.card_pool import CARD_POOL
from games.cards.creature import Creature
from games.mana.mana import Mana
from util.util import flatten


class ExpertTest(TestCase):

    def test_exists_exchanged_low_cost_pair(self):
        self.assertEqual(
            False,
            exists_exchanged_low_cost_pair(
                cast(Creature, CARD_POOL.get_card("3/2(2)")),
                flatten([
                    CARD_POOL.get_card("0/1(1)"),
                    CARD_POOL.get_card("3/7(5)"),
                    CARD_POOL.get_card("1/3(2)"),
                    CARD_POOL.get_card("1/4(2)"),
                ])
            )
        )
        self.assertEqual(
            True,
            exists_exchanged_low_cost_pair(
                cast(Creature, CARD_POOL.get_card("3/2(2)")),
                flatten([
                    CARD_POOL.get_card("0/1(1)"),
                    CARD_POOL.get_card("3/7(5)"),
                    CARD_POOL.get_card("1/3(1)"),
                    CARD_POOL.get_card("1/4(2)"),
                ])
            )
        )

    def test_exists_one_sidedly_destroied_pair(self):
        self.assertEqual(
            False,
            exists_one_sidedly_destroied_pair(
                cast(Creature, CARD_POOL.get_card("3/2(2)")),
                flatten([
                    CARD_POOL.get_card("1/1(1)"),
                    CARD_POOL.get_card("1/4(3)"),
                    CARD_POOL.get_card("0/4(3)"),
                    CARD_POOL.get_card("1/3(2)")
                ])
            )
        )
        self.assertEqual(
            True,
            exists_one_sidedly_destroied_pair(
                cast(Creature, CARD_POOL.get_card("3/2(2)")),
                flatten([
                    CARD_POOL.get_card("1/1(1)"),
                    CARD_POOL.get_card("1/4(3)"),
                    CARD_POOL.get_card("1/3(2)"),
                    CARD_POOL.get_card("1/4(3)"),
                ])
            )
        )

    def test_exists_exchange_high_cost_next_turn(self):
        self.assertEqual(
            False,
            exists_exchange_high_cost_next_turn(
                cast(Creature, CARD_POOL.get_card("3/1(2)")),
                flatten([
                    CARD_POOL.get_card("1/1(1)"),
                    CARD_POOL.get_card("2/3(2)"),
                    CARD_POOL.get_card("0/3(3)"),
                ])
            )
        )
        self.assertEqual(
            True,
            exists_exchange_high_cost_next_turn(
                cast(Creature, CARD_POOL.get_card("3/1(2)")),
                flatten([
                    CARD_POOL.get_card("1/1(1)"),
                    CARD_POOL.get_card("2/3(2)"),
                    CARD_POOL.get_card("1/3(3)"),
                ])
            )
        )

    def test_find_one_sidedly_destroied_smaller_cost_pair(self):
        one_five_four: Tuple[int, Creature] = (0, cast(Creature, CARD_POOL.get_card("1/5(4)")))
        one_four_three: Tuple[int, Creature] = (1, cast(Creature, CARD_POOL.get_card("1/4(3)")))
        self.assertEqual(
            {one_five_four, one_four_three},
            set(
                find_one_sidedly_destroied_smaller_cost_pair(
                    cast(Creature, CARD_POOL.get_card("3/2(2)")),
                    [
                        (5, CARD_POOL.get_card("1/5(6)")),
                        (2, CARD_POOL.get_card("1/1(1)")),
                        one_five_four,
                        (3, CARD_POOL.get_card("2/3(2)")),
                        one_four_three,
                        (4, CARD_POOL.get_card("1/6(7)")),
                    ]
                )
            )
        )

        two_five_four: Tuple[int, Creature] = (0, cast(Creature, CARD_POOL.get_card("2/5(4)")))
        self.assertEqual(
            {two_five_four},
            set(
                find_one_sidedly_destroied_smaller_cost_pair(
                    cast(Creature, CARD_POOL.get_card("1/2(2)")),
                    [
                        (5, CARD_POOL.get_card("1/3(3)")),
                        (2, CARD_POOL.get_card("1/1(1)")),
                        two_five_four,
                        (3, CARD_POOL.get_card("1/2(2)")),
                        one_four_three,
                        (4, CARD_POOL.get_card("1/6(7)")),
                    ]
                )
            )
        )

        two_five_four: Tuple[int, Creature] = (0, cast(Creature, CARD_POOL.get_card("2/5(4)")))
        self.assertEqual(
            {two_five_four},
            set(
                find_one_sidedly_destroied_smaller_cost_pair(
                    cast(Creature, CARD_POOL.get_card("1/2(2)")),
                    [
                        (5, CARD_POOL.get_card("1/2(2)")),
                        (2, CARD_POOL.get_card("1/1(1)")),
                        two_five_four,
                        (3, CARD_POOL.get_card("1/2(2)")),
                        one_four_three,
                        (4, CARD_POOL.get_card("1/6(7)")),
                    ]
                )
            )
        )

    def test_find_exchanged_low_cost_creature(self):
        two_five_four = 0, cast(Creature, CARD_POOL.get_card("2/5(4)")),
        self.assertEqual(
            {two_five_four},
            set(
                find_exchanged_low_cost_creature(
                    cast(Creature, CARD_POOL.get_card("6/2(5)")),
                    [
                        (1, CARD_POOL.get_card("1/2(2)")),
                        (2, CARD_POOL.get_card("1/6(5)")),
                        (3, CARD_POOL.get_card("2/6(6)")),
                        (4, CARD_POOL.get_card("1/6(5)")),
                        two_five_four,
                    ]
                )
            )
        )
        two_two_two: Creature = cast(Creature, CARD_POOL.get_card("2/2(2)"))
        self.assertEqual(
            {(2, two_two_two)},
            set(
                find_exchanged_low_cost_creature(
                    cast(Creature, CARD_POOL.get_card("3/2(3)")),
                    [
                        (1, CARD_POOL.get_card("1/1(1)")),
                        (2, two_two_two)
                    ]
                )
            )
        )

    def test_maximum_playable_creature_count_enough_land(self):
        self.assertEqual(
            4,
            maximum_playable_creature_count_enough_land(
                flatten([
                    CARD_POOL.get_card("1/1(1)", 3),
                    CARD_POOL.get_card("1/2(2)", 4),
                    CARD_POOL.get_card("1/3(3)", 3),
                    CARD_POOL.get_card("1/4(4)", 2),
                    CARD_POOL.get_card("1/5(5)", 2),
                    CARD_POOL.get_card("1/6(6)", 1),
                ]),
                flatten([CARD_POOL.get_card("島", 10)]),
                Mana(num=5)
            )
        )

    def test_count_smallest_pair_exceeds_my_life(self):
        self.assertEqual(
            2,
            count_smallest_pair_exceeds_my_life(
                flatten([
                    CARD_POOL.get_card("1/1(1)", 4),
                    CARD_POOL.get_card("2/2(2)", 2),
                    CARD_POOL.get_card("3/3(3)", 3),
                    CARD_POOL.get_card("4/4(4)", 2),
                ]),
                20
            )
        )

    def test_find_exchanged_creature_pair(self):
        one_one_one: Creature = cast(Creature, CARD_POOL.get_card("1/1(1)"))
        self.assertEqual(
            [(0, one_one_one), (2, one_one_one)],
            find_exchanged_creature_pair(
                cast(Creature, CARD_POOL.get_card("1/2(2)")),
                flatten([
                    (0, one_one_one),
                    (1, CARD_POOL.get_card("3/2(3)")),
                    (2, one_one_one),
                    (3, CARD_POOL.get_card("1/2(2)"))
                ])
            )
        )

    def test_find_damage_destroyable_max_cost_assign(self):
        self.assertEqual(
            [0, 0, 1, 2, 1],
            find_damage_destroyable_max_cost_assign(
                4,
                flatten([
                    (0, CARD_POOL.get_card("6/4(6)")),
                    (1, CARD_POOL.get_card("1/1(1)")),
                    (2, CARD_POOL.get_card("1/1(2)")),
                    (3, CARD_POOL.get_card("3/2(3)")),
                    (4, CARD_POOL.get_card("2/1(1)")),
                ])
            )
        )


if __name__ == "__main__":
    unittest.main()
