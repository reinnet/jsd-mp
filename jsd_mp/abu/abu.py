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
import random


class Abu(Bari):
    n_iter: int = 1000

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

        active_vnfms: typing.Set[str] = set()
        actual_placements: typing.List[
            typing.Tuple[Placement, ManagementPlacement]
        ] = []
        for p, _ in placements:
            mp = self.place_manager(p.chain, self.topology, p)
            if mp is not None:
                self.manage_by_node[mp.management_node] = self.manage_by_node.get(
                    mp.management_node, 0
                ) + len(ch)

                active_vnfms.add(mp.management_node)
                mp.apply_on_topology(self.topology)
                actual_placements.append((p, mp))
            else:
                p.revert_on_topology(self.topology)

        # in each iteration we try to improve the manager placement
        for _ in range(self.n_iter):
            # randomly switch chains between vnfms
            index = random.randint(0, len(actual_placements))
            p, mp = actual_placements[index]
            vnfm = random.choice(list(active_vnfms - set(mp.management_node)))
            mp.revert_on_topology(self.topology)
            if self.is_management_resource_available(self.topology, vnfm, p.nodes):
                paths = []
                for n in p.nodes:
                    path = self.topology.path(vnfm, n, self.vnfm.bandwidth)
                    if path is not None:
                        paths.append(path)
                mp.apply_on_topology(self.topology)
                actual_placements[index] = (
                    p,
                    ManagementPlacement(p.chain, self.vnfm, vnfm, paths),
                )
        return actual_placements

    def place_manager(
        self, chain: Chain, topology: Topology, placement: Placement
    ) -> typing.Union[ManagementPlacement, None]:
        node = ""

        for n in set(placement.nodes):
            if self.is_management_resource_available(topology, n, placement.nodes):
                node = n
                break
        else:
            return None

        paths = []
        for n in placement.nodes:
            path = topology.path(node, n, self.vnfm.bandwidth)
            if path is not None:
                paths.append(path)

        return ManagementPlacement(chain, self.vnfm, node, paths)
