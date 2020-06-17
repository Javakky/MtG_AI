from game.card.Card import Card
from game.card.Permanent import Permanent
from game.card.Spell import Spell


class Creature(Card, Permanent, Spell):
    power: int
    toughness: int
