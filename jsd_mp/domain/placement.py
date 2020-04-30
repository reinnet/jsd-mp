from .nfv import Chain
from .topology import Topology, Link, Node

import dataclasses
import typing


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
