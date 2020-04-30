from config import Config
from domain import Placement, ManagementPlacement

import abc
import typing
import copy
import math


class Solver(abc.ABC):
    """
    Solver solves the placement problem.
    Solver must consider all of the constraints and
    document its shortage or specific use cases.
    Path have direction and management paths goes from manager to nodes.
    """

    def __init__(self, config: Config):
        self.chains = config.chains
        self.vnfm = config.vnfm
        self.topology = copy.deepcopy(config.topology)

        self.manage_by_node: typing.Dict[str, int] = {}
        self.solved: bool = False
        self.solution: typing.List[typing.Tuple[Placement, ManagementPlacement]] = []

    @abc.abstractmethod
    def _solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        pass

    def solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        if self.solved is False:
            self.solution = self._solve()
        return self.solution

    @property
    def cost(self):
        cost = 0
        for manager in self.topology.nodes:
            cost += math.ceil(self.manage_by_node.get(manager, 0) / self.vnfm.capacity)
        return cost

    @property
    def profit(self):
        profit = 0
        for (p, mp) in self.solution:
            profit += p.chain.fee
        return profit
