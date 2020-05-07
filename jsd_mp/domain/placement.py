from .nfv import Chain
from .vnfm import VNFM
from .topology import Topology, Link, Node

import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class ManagementPlacement:
    chain: Chain
    vnfm: VNFM
    management_node: str = ""
    management_links: typing.List[
        typing.List[typing.Tuple[str, str]]
    ] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if sum(self.chain.managebale_functions) != len(self.management_links):
            raise ValueError("Each node of chain must have management link")

    def apply_on_topology(self, topo: Topology):
        node = topo.nodes[self.management_node]
        topo.update_node(
            self.management_node,
            Node(
                cores=node.cores - self.vnfm.cores,
                memory=node.memory - self.vnfm.memory,
                direction=node.direction,
                vnf_support=node.vnf_support,
            ),
        )

        for path in self.management_links:
            for step in path:
                topo.update_link(
                    step[0],
                    step[1],
                    Link(topo.links[step].bandwidth - self.vnfm.bandwidth),
                )

    def revert_on_topology(self, topo: Topology):
        node = topo.nodes[self.management_node]
        topo.update_node(
            self.management_node,
            Node(
                cores=node.cores + self.vnfm.cores,
                memory=node.memory + self.vnfm.memory,
                direction=node.direction,
                vnf_support=node.vnf_support,
            ),
        )

        for path in self.management_links:
            for step in path:
                topo.update_link(
                    step[0],
                    step[1],
                    Link(topo.links[step].bandwidth + self.vnfm.bandwidth),
                )


@dataclasses.dataclass(frozen=True)
class Placement:
    chain: Chain
    nodes: typing.List[str]
    links: typing.Dict[
        typing.Tuple[int, int], typing.List[typing.Tuple[str, str]],
    ]

    def __post_init__(self):
        if len(self.chain.functions) != len(self.nodes):
            raise ValueError("Placement must place every node of the chain")
        for p in self.chain.links:
            if p not in self.links:
                raise ValueError("Placement must place every link of the chain")

    def apply_on_topology(self, topo: Topology):
        for i, n in enumerate(self.nodes):
            node = topo.nodes[n]
            t = self.chain.functions[i]
            topo.update_node(
                n,
                Node(
                    cores=node.cores - t.cores,
                    memory=node.memory - t.memory,
                    direction=node.direction,
                    vnf_support=node.vnf_support,
                ),
            )

        for (source, destination), path in self.links.items():
            link = self.chain.links[(source, destination)]

            for step in path:
                topo.update_link(
                    step[0], step[1], Link(topo.links[step].bandwidth - link.bandwidth)
                )

    def revert_on_topology(self, topo: Topology):
        for i, n in enumerate(self.nodes):
            node = topo.nodes[n]
            t = self.chain.functions[i]
            topo.update_node(
                n,
                Node(
                    cores=node.cores + t.cores,
                    memory=node.memory + t.memory,
                    direction=node.direction,
                    vnf_support=node.vnf_support,
                ),
            )

        for (source, destination), path in self.links.items():
            link = self.chain.links[(source, destination)]

            for step in path:
                topo.update_link(
                    step[0], step[1], Link(topo.links[step].bandwidth + link.bandwidth)
                )
