import math
from typing import Tuple, Optional, NoReturn, TypeVar, List

import numpy

from util.montecalro.config import Config
from util.montecalro.state import State

C = 1.5


class Node:
    def __init__(self, state, config: Config):
        self.state: State = state
        self.w: int = 0
        self.n: int = 0
        self.child_nodes: Optional[Tuple[Node]] = None
        self.config: Config = config

    def evaluate(self) -> float:
        if self.state.end:
            value = self.state.value
            self.w += value
            self.n += 1
            return value

        if not self.child_nodes:
            value = self.state.playout()
            self.w += value
            self.n += 1
            if self.n == self.config.expand:
                self.expand()
        else:
            next: Node = self.next_child_node()
            value = next.evaluate() * (-1 if self.state.switched() else 1)
            self.w += value
            self.n += 1
        return value

    def expand(self) -> NoReturn:
        self.child_nodes = tuple(Node(state.next(), self.config) for state in self.state.legal_actions)

    def next_child_node(self) -> 'Node':
        def ucb1_values() -> Tuple[float]:
            return tuple(
                (child.w / child.n) + self.config.UTC_C * (math.sqrt(math.log2(self.n) / child.n))
                for child in self.child_nodes
            )

        for child_node in self.child_nodes:
            if child_node.n == 0:
                return child_node

        ucb1_values = ucb1_values()

        return self.child_nodes[numpy.array(ucb1_values).argmax()]


N = TypeVar('N', bound=State)


class MCTS:
    def __init__(self, config: Config):
        self.config: Config = config

    def determinization_monte_carlo_tree_search_next_action(self, state: N, config: Config) -> N:
        n: List[int] = [0 for _ in range(len(state.legal_actions))]
        for i in range(self.config.determinizations):
            nexts: Optional[Tuple[Node]] = self.monte_carlo_tree_search(state, config).child_nodes
            for j in range(nexts.__len__()):
                n[j] += nexts[j].n

        return state.legal_actions[
            numpy.array([x for x in n]).argmax()
        ]

    def monte_carlo_tree_search_next_action(self, state: N, config: Config) -> N:
        return state.legal_actions[
            numpy.array([x.n for x in self.monte_carlo_tree_search(state, config).child_nodes]).argmax()
        ]

    def monte_carlo_tree_search(self, state: N, config: Config) -> Node:
        root_node = Node(state, config)
        root_node.expand()

        if root_node.child_nodes.__len__() <= 1:
            return root_node

        for _ in range(self.config.simulations):
            root_node.evaluate()

        return root_node
