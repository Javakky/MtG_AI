from typing import List

from game.card.Card import Card
from game.card.Creature import Creature
from game.card.Land import Land
from game.mana.Color import Color
from game.mana.Mana import Mana

card_pool = [
    Creature("真珠三叉矛の人魚", Mana([Color.Blue]), ["マーフォーク"], 1, 1),
    Land("島", Mana([Color.Blue]))
]


def get_sample_deck() -> List[Card]:
    deck: List[Card] = []
    for i in range(23):
        deck.append()
    for i in range(17):
        deck.append()
    return deck
