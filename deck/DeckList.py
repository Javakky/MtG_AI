from typing import List

from deck.CardPool import CARD_POOL
from game.card.Card import Card
from util.util import flatten


def get_sample_deck() -> List[Card]:
    return flatten([
        CARD_POOL.get_card("真珠三叉矛の人魚", 2),
        CARD_POOL.get_card("志願新兵", 3),
        CARD_POOL.get_card("わら人形の兵士", 3),
        CARD_POOL.get_card("フェメレフの斥候", 2),
        CARD_POOL.get_card("アラボーンの強兵", 3),
        CARD_POOL.get_card("ゴリラの戦士", 2),
        CARD_POOL.get_card("ナナカマドのツリーフォーク", 3),
        CARD_POOL.get_card("トカゲ人間の戦士", 2),
        CARD_POOL.get_card("骸骨クロコダイル"),
        CARD_POOL.get_card("板金鎧のワーム"),
        CARD_POOL.get_card("針刺ワーム"),
        CARD_POOL.get_card("島", 17)
    ])
