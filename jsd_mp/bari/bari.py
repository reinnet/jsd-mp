import typing
import copy
import math
import itertools
from concurrent.futures import ThreadPoolExecutor

from solver import Solver, PartialPlacement
from domain import (
    Placement,
    ManagementPlacement,
    Chain,
    Type,
    Link,
    Topology,
)


class Bari(Solver):
    """
    The Bari algorithm is the modification
    of Md. Faizul Bari (10.1109/TNSM.2016.2569020) algorithm
    for the VNF placement that also place VNFMs.

    This algorithm minimize the cost functions based on DP (Viterbi algorithm)
    in a multi-stage graph. This graph provide feasible nodes in each stage.
    """

    executor = ThreadPoolExecutor(max_workers=100)

    def _solve(
        self,
    ) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        placements: typing.List[
            typing.Tuple[Placement, ManagementPlacement]
        ] = []

        for chain in self.chains:
            self.logger.info("Placement of %s started", chain.name)

            p = self.place(chain)
            if p is not None:
                self.logger.info(
                    "VNF Placement of %s was successful", chain.name
                )

                topo = copy.deepcopy(self.topology)
                p.apply_on_topology(topo)
                mp = self.place_manager(chain, topo, p)
                if mp is not None:
                    self.manage_by_node[
                        mp.management_node
                    ] = self.manage_by_node.get(mp.management_node, 0) + sum(
                        chain.manageable_functions
                    )
                    p.apply_on_topology(self.topology)
                    mp.apply_on_topology(self.topology)
                    placements.append((p, mp))
            else:
                self.logger.info("VNF Placement of %s failed", chain.name)

        return placements

    def place_manager(
        self, chain: Chain, topology: Topology, placement: Placement
    ) -> typing.Union[ManagementPlacement, None]:
        min_cost = float("inf")
        min_node = ""

        for node in topology.nodes:
            if self.is_management_resource_available(
                topology,
                node,
                list(
                    itertools.compress(
                        placement.nodes, chain.manageable_functions
                    )
                ),
            ):
                c = self.get_management_cost(
                    topology,
                    node,
                    list(
                        itertools.compress(
                            placement.nodes, chain.manageable_functions
                        )
                    ),
                )
                if min_cost > c:
                    min_cost = c
                    min_node = node

        if min_cost == float("inf"):
            return None

        paths = []
        for node in itertools.compress(
            placement.nodes, chain.manageable_functions
        ):
            path = topology.path(min_node, node, self.vnfm.bandwidth)
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

            def task(j: str, i: int):
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
                            break

                if min_cost == float("inf"):
                    return
                cost[(i, j)] = int(min_cost)
                path = (
                    pi[(i - 1, min_k)]
                    .apply_on_topology(self.topology)
                    .path(min_k, j, chain.links[(i - 1, i)].bandwidth)
                )
                pi[(i, j)] = pi[(i - 1, min_k)].copy().append(j, path)

            for _ in self.executor.map(
                task, self.topology.nodes, [i for _ in self.topology.nodes]
            ):
                pass

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

    def get_management_cost(
        self,
        topology: Topology,
        manager: str,
        nodes: typing.List[str],
    ) -> int:
        current = math.ceil(
            self.manage_by_node.get(manager, 0) / self.vnfm.capacity
        )
        future = math.ceil(
            (self.manage_by_node.get(manager, 0) + len(nodes))
            / self.vnfm.capacity
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
