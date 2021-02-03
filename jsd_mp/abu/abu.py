import typing
import random
import itertools

from bari import Bari
from domain import (
    Placement,
    ManagementPlacement,
    Chain,
    Topology,
    Node,
)


class Abu(Bari):
    """
    Abu implements the Mohammad Abu-Lebdeh (10.1109/TNSM.2017.2730199)
    tabu search for placing the VNFMs.

    Note that Abu-Lebdeh doesn't mention the VNF placement so we are using
    the Bari solution here for placement.

    If we doesn't provision any resources for VNFMs in the first place,
    this can cause unfeasible solution so we are provisioning resources
    at least one vnfm per node.
    """

    n_iter: int = 1000
    # the precentage of nodes that we are going to reserve VNFM resource on them
    reserve_percentage: int = 100

    def _solve(
        self,
    ) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        placements: typing.List[typing.Tuple[Placement, None]] = []

        self.logger.info(
            "Reserving VNFM resources on %d nodes", self.reserve_percentage
        )
        # we need to reserve resources on nodes for future VNFMs provisioning
        reserved_nodes: typing.List[str] = []
        for id, node in self.topology.nodes.items():
            if (
                node.cores <= self.vnfm.cores
                or node.memory <= self.vnfm.memory
            ):
                continue
            reserved_nodes.append(id)
            if random.randint(0, 100) > self.reserve_percentage:
                continue
            self.topology.update_node(
                id,
                Node(
                    cores=node.cores - self.vnfm.cores,
                    memory=node.memory - self.vnfm.memory,
                    direction=node.direction,
                    vnf_support=node.vnf_support,
                ),
            )

        # place chains with Bari algorithm
        for chain in self.chains:
            self.logger.info("Placement of %s started", chain.name)

            p = self.place(chain)
            if p is not None:
                self.logger.info(
                    "VNF Placement of %s was successful", chain.name
                )
                p.apply_on_topology(self.topology)
                placements.append((p, None))
            else:
                self.logger.info("VNF Placement of %s failed", chain.name)

        # valid placements are the placements which has their
        # manager on one of their's node.
        actual_placements: typing.List[
            typing.Tuple[Placement, ManagementPlacement]
        ] = []

        # take the reserved resources back to provision the VNFMs
        for id in reserved_nodes:
            node = self.topology.nodes[id]
            self.topology.update_node(
                id,
                Node(
                    cores=node.cores + self.vnfm.cores,
                    memory=node.memory + self.vnfm.memory,
                    direction=node.direction,
                    vnf_support=node.vnf_support,
                ),
            )

        # find manager placement for each placed chain
        for p, _ in placements:
            mp = self.place_manager(p.chain, self.topology, p)
            if mp is not None:
                self.manage_by_node[
                    mp.management_node
                ] = self.manage_by_node.get(mp.management_node, 0) + sum(
                    p.chain.manageable_functions
                )

                mp.apply_on_topology(self.topology)
                actual_placements.append((p, mp))
            else:
                p.revert_on_topology(self.topology)

        # in each iteration we try to improve the manager placement
        for _ in range(self.n_iter):
            current_cost = self.cost

            # randomly switch chains between vnfms
            index = random.randint(0, len(actual_placements) - 1)
            p, mp = actual_placements[index]
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
                    actual_placements[index] = (
                        p,
                        new_mp,
                    )
            else:
                self.apply_management(mp)

        return actual_placements

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

    def place_manager(
        self, chain: Chain, topology: Topology, placement: Placement
    ) -> typing.Union[ManagementPlacement, None]:
        node = ""

        for n in set(
            itertools.compress(placement.nodes, chain.manageable_functions)
        ):
            if self.is_management_resource_available(
                topology,
                n,
                list(
                    itertools.compress(
                        placement.nodes, chain.manageable_functions
                    )
                ),
            ):
                node = n
                break
        else:
            return None

        paths = []
        for n in itertools.compress(
            placement.nodes, placement.chain.manageable_functions
        ):
            path = topology.path(node, n, self.vnfm.bandwidth)
            if path is not None:
                paths.append(path)

        return ManagementPlacement(chain, self.vnfm, node, paths)
