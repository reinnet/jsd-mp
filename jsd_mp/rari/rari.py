from bari import Bari
from solver import Solver, Random
from config import Config
from domain import (
    Placement,
    ManagementPlacement,
)

import typing


class Rari(Solver):
    def _solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        placements: typing.List[typing.Tuple[Placement, ManagementPlacement]] = []

        random = Random(Config({}, self.chains, self.vnfm, self.topology))
        placements.extend(random.solve())
        for node, count in random.manage_by_node.items():
            self.manage_by_node[node] = count

        self.logger.info(
            "Random place %d chains of %d", len(placements), len(self.chains)
        )
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

        return placements
