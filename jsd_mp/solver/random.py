"""
random solver place chains with randomly.
"""
import typing
import random
import itertools

from domain import (
    Placement,
    ManagementPlacement,
    Direction,
)
from .placement import PartialPlacement
from .solver import Solver


class Random(Solver):
    def _solve(
        self,
    ) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        placements: typing.List[
            typing.Tuple[Placement, ManagementPlacement]
        ] = []

        for chain in self.chains:
            topology = self.topology
            pp = PartialPlacement(chain)

            for i, function in enumerate(chain.functions):
                candidates = [
                    name
                    for (name, node) in topology.nodes.items()
                    if node.memory >= function.memory
                    and node.cores >= function.cores
                    and node.vnf_support
                    and (
                        function.direction is node.direction
                        or node.direction is Direction.BOTH
                    )
                ]
                if len(candidates) == 0:
                    break

                n: str = random.choice(candidates)

                if self.is_resource_available(
                    topology,
                    "" if i == 0 else pp.nodes[i - 1],
                    n,
                    function,
                    None if i == 0 else chain.links[(i - 1, i)],
                ):
                    if i > 0:
                        path = topology.path(
                            pp.nodes[i - 1],
                            n,
                            chain.links[(i - 1, i)].bandwidth,
                        )
                        if path is not None:
                            pp.append(n, path)
                        else:
                            break
                    else:
                        pp.append(n, None)
                    topology = pp.apply_on_topology(self.topology)
                else:
                    break
            else:
                management_node: str = random.choice(
                    [
                        name
                        for (name, node) in topology.nodes.items()
                        if node.memory >= self.vnfm.memory
                        and node.cores >= self.vnfm.cores
                        and node.vnf_support
                    ]
                )
                if not self.is_management_resource_available(
                    topology,
                    management_node,
                    list(
                        itertools.compress(
                            pp.nodes, chain.manageable_functions
                        )
                    ),
                ):
                    continue
                management_paths = []
                for n in itertools.compress(
                    pp.nodes, chain.manageable_functions
                ):
                    path = self.topology.path(
                        management_node, n, self.vnfm.bandwidth
                    )
                    if path is not None:
                        management_paths.append(path)
                    else:
                        break
                else:
                    p = Placement(chain, pp.nodes, pp.links)
                    p.apply_on_topology(self.topology)
                    mp = ManagementPlacement(
                        chain, self.vnfm, management_node, management_paths
                    )
                    self.manage_by_node[
                        management_node
                    ] = self.manage_by_node.get(management_node, 0) + sum(
                        chain.manageable_functions
                    )
                    mp.apply_on_topology(self.topology)
                    placements.append((p, mp))

        return placements
