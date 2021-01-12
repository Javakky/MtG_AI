from math import log
from typing import Tuple, Optional, NoReturn

import numpy

from util.montecalro.state import State


class Node:
    def __init__(self, state):
        self.state: State = state
        self.w: int = 0
        self.n: int = 0
        self.child_nodes: Optional[Tuple[Node]] = None

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
            if self.n == 10:
                self.expand()
        else:
            next: Node = self.next_child_node()
            value = self.next_child_node().evaluate()
            self.w += value
            self.n += 1
        return value

    def expand(self) -> NoReturn:
        self.child_nodes = tuple(Node(self.state.next(action)) for action in self.state.legal_actions)

    def next_child_node(self) -> 'Node':
        def ucb1_values() -> Tuple[float]:
            t = sum([i.n for i in self.child_nodes])
            return tuple(
                -child.w / child.n + 2 * (2 * log(t) / child.n) ** 0.5
                for child in self.child_nodes
            )

        for child_node in self.child_nodes:
            if child_node.n == 0:
                return child_node

        ucb1_values = ucb1_values()

        return self.child_nodes[numpy.array(ucb1_values).argmax()]
