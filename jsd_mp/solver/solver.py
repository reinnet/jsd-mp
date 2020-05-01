from config import Config
from domain import Placement, ManagementPlacement, Topology, Link, Type, Direction

import abc
import typing
import copy
import math
import logging


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

        self.logger: logging.Logger = logging.getLogger(__name__)

        self.manage_by_node: typing.Dict[str, int] = {}
        self.solved: bool = False
        self.solution: typing.List[typing.Tuple[Placement, ManagementPlacement]] = []

    @abc.abstractmethod
    def _solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        pass

    def solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        self.logger.info(f"{self.__class__.__name__} Started")
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

    def is_management_resource_available(
        self, topology: Topology, manager: str, nodes: typing.List[str],
    ) -> bool:
        node = topology.nodes[manager]

        if node.memory < self.vnfm.memory:
            return False

        if node.cores < self.vnfm.cores:
            return False

        r = topology.bfs(manager, self.vnfm.bandwidth)

        for node in nodes:
            for (destination, height) in r:
                if destination == node and height <= self.vnfm.radius:
                    break
            else:
                return False
        return True

    @staticmethod
    def is_resource_available(
        topology: Topology,
        previous: str,
        current: str,
        fn: Type,
        link: typing.Union[Link, None],
    ) -> bool:
        """
        Check the availability of current node for the given function.
        This function consider the previous node for finding a path from it
        to the current node.
        """
        node = topology.nodes[current]

        if node.memory < fn.memory:
            return False

        if node.cores < fn.cores:
            return False

        if node.vnf_support is False:
            return False

        if fn.direction is Direction.INGRESS:
            if node.direction is Direction.NONE or node.direction is Direction.EGRESS:
                return False

        if fn.direction is Direction.EGRESS:
            if node.direction is Direction.NONE or node.direction is Direction.INGRESS:
                return False

        if previous != "" and link is not None:
            if topology.path(previous, current, link.bandwidth) is None:
                return False

        return True
