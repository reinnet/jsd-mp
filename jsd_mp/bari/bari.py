from solver import Solver
from domain import (
    Placement,
    ManagementPlacement,
    Chain,
    Type,
    Direction,
    Link,
    Topology,
)
from .placement import PartialPlacement

import typing
import copy
import math


class Bari(Solver):
    def _solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        placements: typing.List[typing.Tuple[Placement, ManagementPlacement]] = []

        for ch in self.chains:
            p = self.place(ch)
            if p is not None:
                topo = copy.deepcopy(self.topology)
                p.apply_on_topology(topo)
                mp = self.place_manager(ch, topo, p)
                if mp is not None:
                    self.manage_by_node[mp.management_node] = self.manage_by_node.get(
                        mp.management_node, 0
                    ) + len(ch)
                    p.apply_on_topology(self.topology)
                    mp.apply_on_topology(self.topology)
                    placements.append((p, mp))

        return placements

    def place_manager(
        self, chain: Chain, topology: Topology, placement: Placement
    ) -> typing.Union[ManagementPlacement, None]:
        min_cost = float("inf")
        min_node = ""

        for n in topology.nodes:
            if self.is_management_resource_available(topology, n, placement.nodes):
                c = self.get_management_cost(topology, n, placement.nodes)
                if min_cost > c:
                    min_cost = c
                    min_node = n

        if min_cost == float("inf"):
            return None

        paths = []
        for n in placement.nodes:
            path = topology.path(min_node, n, self.vnfm.bandwidth)
            if path is not None:
                paths.append(path)

        return ManagementPlacement(chain, self.vnfm, min_node, paths)

    def place(self, chain: Chain) -> typing.Union[Placement, None]:
        # cost represents the cumulative cost of placing the i-th function
        # on the node j. The cost is updated on each step of chain placement.
        cost: typing.Dict[typing.Tuple[int, str], int] = {}
        pi: typing.Dict[typing.Tuple[int, str], PartialPlacement] = {}

        # place the ingress function
        for n in self.topology.nodes:
            if self.is_resource_available(
                self.topology, "", n, chain.functions[0], None
            ):
                cost[(0, n)] = self.get_cost(
                    self.topology, "", n, chain.functions[0], None
                )
                pi[(0, n)] = PartialPlacement(chain).append(n, None)

        # place rest of the functions
        for i in range(1, len(chain.functions)):
            for j in self.topology.nodes:
                min_cost = float("inf")
                min_k = ""

                for k in self.topology.nodes:
                    if (i - 1, k) in pi and self.is_resource_available(
                        pi[(i - 1, k)].apply_on_topology(self.topology),
                        k,
                        j,
                        chain.functions[i],
                        chain.links[(i - 1, i)],
                    ):
                        c = self.get_cost(
                            pi[(i - 1, k)].apply_on_topology(self.topology),
                            k,
                            j,
                            chain.functions[i],
                            chain.links[(i - 1, i)],
                        )
                        if min_cost > c:
                            min_cost = c
                            min_k = k

                if min_cost == float("inf"):
                    continue
                cost[(i, j)] = int(min_cost)
                path = (
                    pi[(i - 1, min_k)]
                    .apply_on_topology(self.topology)
                    .path(min_k, j, chain.links[(i - 1, i)].bandwidth)
                )
                pi[(i, j)] = pi[(i - 1, min_k)].copy().append(j, path)

        # find the minimum cost of placement
        min_cost = float("inf")
        min_placement = None

        for pair, c in cost.items():
            if len(pi[pair].nodes) == len(chain):
                if min_cost > c:
                    min_placement = pi[pair]

        if min_placement is None:
            return None
        return Placement(chain, min_placement.nodes, min_placement.links)

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

    def get_management_cost(
        self, topology: Topology, manager: str, nodes: typing.List[str],
    ) -> int:
        current = math.ceil(self.manage_by_node.get(manager, 0) / self.vnfm.capacity)
        future = math.ceil(
            (self.manage_by_node.get(manager, 0) + len(nodes)) / self.vnfm.capacity
        )
        return future - current

    @staticmethod
    def get_cost(
        topology: Topology,
        previous: str,
        current: str,
        fn: Type,
        link: typing.Union[Link, None],
    ) -> int:
        return 0

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
