from typing import List, Dict, Optional, cast, Tuple

from client.console_user import ConsoleUser, print_cards
from deck.deck_list import get_sample_deck
from games.cards.card import Card
from games.cards.creature import Creature
from games.cards.land import Land
from games.game import Game
from games.mana.mana import Mana


class Expert(ConsoleUser):

    def __init__(self, game: Game, name: str):
        super().__init__(game, name)

    def get_deck(self) -> List[Card]:
        return get_sample_deck()

    def choose_play_first(self):
        self.game.choose_play_first(self, True)

    def draw_starting_hand(self, hands: List[Card]):
        print("【" + self.name + "】の初期手札 " + str(len(hands)) + "枚：")
        print_cards(hands)
        print()

    def chosen_play_first(self, play_first: bool):
        pass

    def upkeep_step(self):
        pass

    def draw_step(self, card: Card):
        self.print_hand()
        self.game.finish_main_phase()

    def combat_damage(self, result: Dict):
        pass

    def ending_the_game(self, win: bool):
        pass

    def receive_priority(self):
        if not self.game.played_land():
            lands: List[Tuple[int, Land]] = self.game.get_indexed_hands(self, Land)
            if lands.__len__() > 0:
                print("【" + self.name + "】が土地をプレイしました：")
                print_cards([lands[0][1]])
                self.game.play_land(lands[0][0])
                return

        creatures: List[Tuple[int, Creature]] = self.game.get_indexed_hands(self, Creature)
        lands: List[Tuple[int, Land]] = self.game.get_indexed_fields(self, Land)
        remain_mana: Mana = self.game.get_remain_mana()
        most_large_cost_creature: Optional[Creature] = None
        creature_index: int = -1
        for tpl in creatures:
            if remain_mana.contains(tpl[1].mana_cost) and \
                    (most_large_cost_creature is None
                     or most_large_cost_creature.mana_cost.count() < tpl[1].mana_cost.count()):
                most_large_cost_creature = cast(Creature, tpl[1])
                creature_index = tpl[0]
        if most_large_cost_creature is not None:
            land_indexes: List[int] = []
            tapped_lands: List[Land] = []
            genelated_mana: int = 0
            creature_mana: int = most_large_cost_creature.mana_cost.count()
            for land in lands:
                if creature_mana > genelated_mana:
                    land_indexes.append(land[0])
                    print(str(land[0]) + ":" + land[1].__str__())
                    tapped_lands.append(land[1])
                    genelated_mana += land[1].mana.count()
            self.print_field()
            print("【" + self.name + "】がクリーチャーをプレイしました：")
            print_cards([most_large_cost_creature])
            print("土地をタップしました：")
            print_cards(tapped_lands)
            self.game.cast_pay_cost(creature_index, land_indexes)
        else:
            self.game.pass_priority()

    def declare_attackers_step(self):
        self.game.declare_attackers([])

    def declare_blockers_step(self, attackers: List[int]):
        for attacker in attackers:
            self.game.declare_blokers(attacker, [])
        self.game.combat_damage()

    def assign_damage(self, attacker: int, blockers: List[int]):
        pass
