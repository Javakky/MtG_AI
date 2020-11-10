from typing import Dict, List, Union

from game.card.Card import Card
from game.card.CardType import CardType
from game.card.Creature import Creature
from game.card.Land import Land
from game.mana.Color import Color
from game.mana.Mana import Mana
from util.Exception import IllegalNumberException


class CardPool:
    def __init__(self):
        self.pool: Dict[str, Card] = {}
        self.creatures: List[Card] = []
        self.lands: List[Card] = []

    def get_card(self, name: str, num: int = 1) -> Union[Card, List[Card]]:
        if num < 1:
            raise IllegalNumberException()
        if num == 1:
            return self.pool[name].clone()
        cards: List[Card] = []
        for i in range(num):
            cards.append(self.pool[name].clone())
        return cards

    def add_card(self, value: Card):
        self.pool[value.name] = value
        if value.type() == CardType.CREATURE:
            self.creatures.append(value)
        elif value.type() == CardType.LAND:
            self.lands.append(value)


CARD_POOL: CardPool = CardPool()

# 1コスト
CARD_POOL.add_card(Creature("真珠三叉矛の人魚", Mana([Color.COLORLESS]), ["マーフォーク"], 1, 1))  # 青
# 2コスト
CARD_POOL.add_card(Creature("志願新兵", Mana([Color.COLORLESS], 1), ["人間", "レベル"], 2, 2))  # 白
CARD_POOL.add_card(Creature("わら人形の兵士", Mana([Color.COLORLESS], 1), ["カカシ", "兵士"], 1, 3))  # 白
# 3コスト
CARD_POOL.add_card(Creature("フェメレフの斥候", Mana([Color.COLORLESS], 2), ["人間", "スカウト"], 1, 4))  # 白
CARD_POOL.add_card(Creature("アラボーンの強兵", Mana([Color.COLORLESS], 2), ["人間", "兵士"], 2, 3))  # 白
CARD_POOL.add_card(Creature("ゴリラの戦士", Mana([Color.COLORLESS], 2), ["類人猿", "戦士"], 3, 2))  # 緑
# 4コスト
CARD_POOL.add_card(Creature("ナナカマドのツリーフォーク", Mana([Color.COLORLESS], 3), ["ツリーフォーク"], 3, 4))  # 緑
CARD_POOL.add_card(Creature("トカゲ人間の戦士", Mana([Color.COLORLESS], 3), ["トカゲ", "戦士"], 4, 2))  # 赤
CARD_POOL.add_card(Creature("骸骨クロコダイル", Mana([Color.COLORLESS], 3), ["クロコダイル", "スケルトン"], 5, 1))  # 黒
# 5コスト
CARD_POOL.add_card(Creature("板金鎧のワーム", Mana([Color.COLORLESS], 4), ["ワーム"], 4, 5))  # 緑
CARD_POOL.add_card(Creature("針刺ワーム", Mana([Color.COLORLESS], 4), ["ワーム"], 5, 4))  # 緑
CARD_POOL.add_card(Creature("豹の戦士", Mana([Color.COLORLESS], 4), ["猫", "戦士"], 6, 3))  # 緑
CARD_POOL.add_card(Creature("レッドウッド・ツリーフォーク", Mana([Color.COLORLESS], 4), ["ツリーフォーク"], 3, 6))  # 緑
# 6コスト
CARD_POOL.add_card(Creature("黒曜石のゴーレム", Mana(num=6), ["ゴーレム"], 4, 6))  # アーティファクト クリーチャー
CARD_POOL.add_card(Creature("棘状歯のワーム", Mana([Color.COLORLESS], 5), ["ワーム"], 6, 4))  # 緑
# 7コスト
CARD_POOL.add_card(Creature("ヴィザードリックス", Mana([Color.COLORLESS], 6), ["兎", "ビースト"], 6, 6))  # 青
# 土地
CARD_POOL.add_card(Land("島", Mana([Color.BLUE])))
