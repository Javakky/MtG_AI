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

    def set_order(self, order: List[Card]):
        deck: List[Card] = []
        for card in order:
            deck.append(self.library.pop(card.name))
        self.library.cards = deck

    def first_draw(self) -> List[Card]:
        cards: List[Card] = []
        for i in range(7):
            cards.append(self.draw())
        return cards

    def draw(self) -> Optional[Card]:
        card: Card = self.library.pop()
        self.hand.append(card)
        return card

    def play(self, index: int) -> NoReturn:
        card = self.hand.get(index)
        if isinstance(card, Land):
            self.play_land(index)
        elif isinstance(card, Spell):
            self.cast(index)

    def play_land(self, index: int) -> NoReturn:
        if self.played_land:
            raise IllegalPlayLandException("このターン既に土地はプレイされています")
        self.field.append(self.hand.pop_index(index, Land))
        self.played_land = True

    def cast_pay_cost(self, spell_index: int, manabase_indexes: List[int]) -> NoReturn:
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
        self.field.append(self.hand.pop_index(spell_index, Permanent))

    def cast(self, index: int) -> NoReturn:
        if isinstance(self.hand.get(index), Permanent):
            self.field.append(self.hand.pop_index(index, Permanent))

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
        tmp = self.field.pop_index(index, type)
        self.graveyard.append(tmp)
        return tmp

    def get_hands(self, type: Type[C] = Card) -> List[C]:
        return self.hand.get_all(type)

    def get_graveyards(self, type: Type[C] = Card) -> List[C]:
        return self.graveyard.get_all(type)

    def get_hand(self, index: int, type: Type[P] = Permanent) -> P:
        return self.hand.get(index, type)

    def untap_all(self) -> NoReturn:
        self.field.untap_all()
        self.played_land = False

    def damage(self, power) -> int:
        self.life = self.life - power
        return self.life

    def get_field(self, index: int, type: Type[P] = Permanent) -> P:
        return self.field.get(index, type)

    def get_fields(self, indexes: List[int] = None, type: Type[P] = Permanent) -> List[P]:
        if indexes is None:
            return self.field.get_cards(type=type)
        return self.field.get(indexes, type)

    def get_remain_mana(self) -> int:
        return self.field.get_remain_mana()

    def get_life(self) -> int:
        return self.life

    def get_library_count(self) -> int:
        return self.library.cards.__len__()
