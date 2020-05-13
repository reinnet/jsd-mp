from bari import Bari
from solver import Solver, Random
from config import Config
from domain import (
    Placement,
    ManagementPlacement,
)

import typing
import random
import math
import itertools


class Rari(Solver):
    n_iter: int = 100

    def _solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        placements: typing.List[typing.Tuple[Placement, ManagementPlacement]] = []

        rnd_index = math.ceil(len(self.chains) / 2)

        rnd = Random(Config({}, self.chains[:rnd_index], self.vnfm, self.topology))
        placements.extend(rnd.solve())
        for node, count in rnd.manage_by_node.items():
            self.manage_by_node[node] = count

        self.logger.info("Random place %d chains of %d", len(placements), rnd_index)
        placed_chains = [p.chain for (p, _) in placements]

        bari = Bari(
            Config(
                {},
                [chain for chain in self.chains if chain not in placed_chains],
                self.vnfm,
                self.topology,
            )
        )
        placements.extend(bari.solve())
        for node, count in bari.manage_by_node.items():
            self.manage_by_node[node] = self.manage_by_node.get(node, 0) + count

        self.logger.info(
            "Bari place %d chains of remaining %d",
            len(placements) - len(placed_chains),
            len(self.chains) - len(placed_chains),
        )

        # in each iteration we try to improve the manager placement
        for _ in range(self.n_iter):
            current_cost = self.cost

            # randomly switch chains between vnfms
            index = random.randint(0, len(placements) - 1)
            p, mp = placements[index]
            # each node can be a manager if it has the required resources
            vnfm = random.choice(
                list(
                    set(self.topology.nodes)
                    - (set(mp.management_node) if mp is not None else set())
                )
            )

            # revert the current manager placement
            self.revert_management(mp)

            # find new manager placement
            manageable_functions = list(
                itertools.compress(p.nodes, p.chain.manageable_functions)
            )
            if self.is_management_resource_available(
                self.topology, vnfm, manageable_functions
            ):
                paths = []
                for n in manageable_functions:
                    path = self.topology.path(vnfm, n, self.vnfm.bandwidth)
                    if path is not None:
                        paths.append(path)
                new_mp = ManagementPlacement(p.chain, self.vnfm, vnfm, paths)

                # apply new manager placement
                self.apply_management(new_mp)

                if self.cost > current_cost:
                    self.revert_management(new_mp)
                    self.apply_management(mp)
                else:
                    # update the placement
                    placements[index] = (
                        p,
                        new_mp,
                    )
            else:
                self.apply_management(mp)

        return placements

    def apply_management(self, mp: ManagementPlacement):
        mp.apply_on_topology(self.topology)
        self.manage_by_node[mp.management_node] = self.manage_by_node.get(
            mp.management_node, 0
        ) + len(mp.management_links)

    def revert_management(self, mp: ManagementPlacement):
        mp.revert_on_topology(self.topology)
        self.manage_by_node[mp.management_node] = self.manage_by_node.get(
            mp.management_node, 0
        ) - len(mp.management_links)
