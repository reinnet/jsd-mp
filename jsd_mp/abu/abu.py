from bari import Bari
from domain import (
    Placement,
    ManagementPlacement,
    Chain,
    Type,
    Link,
    Topology,
)

import typing


class Abu(Bari):
    def _solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        placements: typing.List[typing.Tuple[Placement, None]] = []

        for ch in self.chains:
            self.logger.info(f"Placement of {ch.name} started")

            p = self.place(ch)
            if p is not None:
                self.logger.info(f"VNF Placement of {ch.name} was successful")
                p.apply_on_topology(self.topology)
                placements.append((p, None))
            else:
                self.logger.info(f"VNF Placement of {ch.name} failed")

        actual_placements: typing.List[
            typing.Tuple[Placement, ManagementPlacement]
        ] = []
        for p, _ in placements:
            mp = self.place_manager(p.chain, self.topology, p)
            if mp is not None:
                mp.apply_on_topology(self.topology)
                actual_placements.append((p, mp))
            else:
                pass  # TODO: put the chain's resources back

    def place_manager(
        self, chain: Chain, topology: Topology, placement: Placement
    ) -> typing.Union[ManagementPlacement, None]:
        min_node = ""

        for n in set(placement.nodes):
            if self.is_management_resource_available(topology, n, placement.nodes):
                min_node = n
                break
        else:
            return None

        paths = []
        for n in placement.nodes:
            path = topology.path(min_node, n, self.vnfm.bandwidth)
            if path is not None:
                paths.append(path)

        return ManagementPlacement(chain, self.vnfm, min_node, paths)
