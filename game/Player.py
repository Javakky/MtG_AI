from game.Battlefield import *
from game.Graveyard import *
from game.Hand import *
from game.Library import *
from game.card.Creature import Creature
from game.card.Land import Land
from game.card.ManaBase import ManaBase
from game.card.Spell import Spell
from game.mana.Mana import Mana
from util.Exception import IllegalManaException, IllegalPlayLandException


class Player:
    P = TypeVar('P', bound=Permanent)

    def __init__(self, deck: List[Card]):
        self.hand: Hand = Hand()
        self.library = Library(deck)
        self.field: Battlefield = Battlefield()
        self.graveyard: Graveyard = Graveyard()
        self.life: int = 20
        self.played_land: bool = False
        self.library.shuffle()
        for i in range(7):
            self.draw()

    def draw(self) -> Optional[Card]:
        card: Card = self.library.pop()
        self.hand.append(card)
        return card

    def play(self, index: int):
        card = self.hand.get(index)
        if isinstance(card, Land):
            self.play_land(index)
        elif isinstance(card, Spell):
            self.cast(index)

    def play_land(self, index: int):
        if self.played_land:
            raise IllegalPlayLandException("このターン既に土地はプレイされています")
        self.field.append(self.hand.pop(index, Land))
        self.played_land = True

    def cast_pay_cost(self, spell_index: int, manabase_indexes: List[int]):
        mana_cost: Mana = Mana([])
        for i in manabase_indexes:
            if not self.field.get(i, ManaBase).untapped:
                raise IllegalManaException("このパーマネントは既にタップされています: "
                                           "[index => " + str(i) + ", name => " + self.field.get(i).name + "]")
            mana_cost.extend(self.field.get(i, ManaBase).addable_symbols())
        if not self.hand.get(spell_index, Spell).legal_mana_cost(mana_cost):
            raise IllegalManaException("マナが足りません")
        for i in manabase_indexes:
            self.field.tap(i, Land)
        self.field.append(self.hand.pop(spell_index, Permanent))

    def cast(self, index: int):
        if isinstance(self.hand.get(index), Permanent):
            self.field.append(self.hand.pop(index, Permanent))

    def declare_attackers(self, indexes: List[int]) -> List[int]:
        tmp_attacker = []
        for i in indexes:
            if self.field.is_untapped(i, Creature):
                self.field.tap(i, Creature)
                tmp_attacker.append(i)
        return tmp_attacker

    def declare_blockers(self, blocker_indexes: List[int]) -> List[int]:
        tmp_blocker = []
        for i in blocker_indexes:
            if self.field.is_untapped(i, Creature):
                self.field.tap(i, Creature)
                tmp_blocker.append(i)
        return tmp_blocker

    def destroy(self, index: int, type: Type[P] = Permanent) -> P:
        tmp = self.field.pop(index, type)
        self.graveyard.append(tmp)
        return tmp

    def get_hands(self) -> List[Card]:
        return self.hand.cards

    def get_hand(self, index: int, type: Type[P] = Permanent) -> P:
        return self.hand.get(index, type)

    def untap_all(self):
        self.field.untap_all()
        self.played_land = False

    def damage(self, power) -> int:
        self.life = self.life - power
        return self.life

    def get_field(self, index: int, type: Type[P] = Permanent) -> P:
        return self.field.get(index, type)

    def get_fields(self, indexes: List[int] = None, type: Type[P] = Permanent) -> List[P]:
        if indexes:
            return self.field.get_all(type)
        return self.field.get(indexes, type)
