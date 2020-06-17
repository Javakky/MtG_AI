from game.Battlefield import *
from game.Graveyard import *
from game.Hand import *
from game.Library import *
from game.card.Creature import Creature
from game.card.Land import Land
from game.card.ManaBase import ManaBase
from game.card.Spell import Spell
from game.mana.Mana import Mana
from util.Exception import IllegalManaException


class Player:
    hand: Hand = Hand()
    library: Library
    field: Battlefield = Battlefield()
    graveyard: Graveyard = Graveyard()
    life: int = 20
    P = TypeVar('P', bound=Permanent)

    def __init__(self, deck: List[Card]):
        self.library = Library(deck)
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
        self.field.append(self.hand.pop(index, Land))

    def cast_pay_cost(self, spell_index: int, manabase_indexes: List[int]):
        mana_cost: Mana = Mana([])
        for i in manabase_indexes:
            if not self.field.get(i, ManaBase).untapped:
                raise IllegalManaException("このパーマネントは既にタップされています: "
                                           "[index => " + str(i) + ", name => " + self.field.get(i).name + "]")
            mana_cost.extend(self.field.get(i, ManaBase).addable_symbols())
        if not self.field.get(spell_index, Spell).legal_mana_cost(mana_cost):
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

    def destroy(self, index: int, type: Type[P] = Permanent):
        self.graveyard.append(self.field.pop(index, type))

    def get_hands(self) -> List[Card]:
        return self.hand.cards

    def untap_all(self):
        self.field.untap_all()

    def damage(self, power) -> int:
        self.life = self.life - power
        return self.life

    def get_field(self, index: int, type: Type[P] = Permanent) -> P:
        return self.field.get(index, type)

    def get_fields(self, indexes: List[int] = None, type: Type[P] = Permanent) -> List[P]:
        if indexes:
            return self.field.get_all(type)
        return self.field.get(indexes, type)
