from __future__ import annotations

import dataclasses
import typing
import copy

from domain import Topology, Chain, Node, Link


@dataclasses.dataclass(frozen=True)
class PartialPlacement:
    chain: Chain
    nodes: typing.List[str] = dataclasses.field(default_factory=list)
    links: typing.Dict[
        typing.Tuple[int, int], typing.List[typing.Tuple[str, str]],
    ] = dataclasses.field(default_factory=dict)

    def append(
        self, node: str, path: typing.Union[typing.List[typing.Tuple[str, str]], None]
    ) -> PartialPlacement:
        self.nodes.append(node)
        if len(self.nodes) > 1 and path is not None:
            self.links[(len(self.nodes) - 2, len(self.nodes) - 1)] = path
        return self

    def copy(self) -> PartialPlacement:
        return copy.deepcopy(self)

    def apply_on_topology(self, topology: Topology) -> Topology:
        topo = copy.deepcopy(topology)

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

        return topo
