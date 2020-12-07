from games.battlefield import *
from games.cards.creature import Creature
from games.cards.land import Land
from games.cards.mana_base import ManaBase
from games.cards.spell import Spell
from games.graveyard import *
from games.hand import *
from games.library import *
from games.mana.mana import Mana
from util.Exception import IllegalManaException, IllegalPlayLandException


class Player:
    P = TypeVar('P', bound=Permanent)
    C = TypeVar('C', bound=Card)

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
            mana_cost += self.field.get(i, ManaBase).addable_symbols()
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

    def get_hands(self, type: Type[C] = Card) -> List[C]:
        return self.hand.get_all(type)

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
            return self.field.get_cards(type)
        return self.field.get(indexes, type)

    def get_remain_mana(self) -> Mana:
        return self.field.get_remain_mana()

    def get_life(self) -> int:
        return self.life
