import typing
import dataclasses

from .nfv import Chain
from .vnfm import VNFM
from .topology import Topology, Link, Node


@dataclasses.dataclass(frozen=True)
class ManagementPlacement:
    chain: Chain
    vnfm: VNFM
    management_node: str = ""
    management_links: typing.List[
        typing.List[typing.Tuple[str, str]]
    ] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if sum(self.chain.manageable_functions) != len(self.management_links):
            raise ValueError("Each node of chain must have management link")

    def __repr__(self):
        repr = ""
        repr += f"manage by {self.management_node}\n"

        for i, path in enumerate(self.management_links):
            repr += f"management route of function-{i}:\n"
            for (source, sink) in path:
                repr += f"\t{source} -> {sink}\n"

        return repr

    def apply_on_topology(self, topo: Topology):
        node = topo.nodes[self.management_node]
        topo.update_node(
            self.management_node,
            Node(
                cores=node.cores - self.vnfm.cores,
                memory=node.memory - self.vnfm.memory,
                direction=node.direction,
                vnf_support=node.vnf_support,
                not_manager_nodes=node.not_manager_nodes,
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
                not_manager_nodes=node.not_manager_nodes,
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
        typing.Tuple[int, int],
        typing.List[typing.Tuple[str, str]],
    ]

    def __post_init__(self):
        if len(self.chain.functions) != len(self.nodes):
            raise ValueError("Placement must place every node of the chain")
        for p in self.chain.links:
            if p not in self.links:
                raise ValueError(
                    "Placement must place every link of the chain"
                )

    def __repr__(self):
        repr = ""
        for i, node in enumerate(self.nodes):
            repr += f"funcion-{i} [{self.chain.functions[i].name}] is placed on {node}\n"

        for (from_function, to_function), path in self.links.items():
            repr += (
                f"function-{from_function} -> function-{to_function}"
                " is placed on the following links:\n"
            )
            for (source, sink) in path:
                repr += f"\t{source} -> {sink}\n"
        return repr

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
                    not_manager_nodes=node.not_manager_nodes,
                ),
            )

        for (source, destination), path in self.links.items():
            link = self.chain.links[(source, destination)]

            for step in path:
                topo.update_link(
                    step[0],
                    step[1],
                    Link(topo.links[step].bandwidth - link.bandwidth),
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
                    not_manager_nodes=node.not_manager_nodes,
                ),
            )

        for (source, destination), path in self.links.items():
            link = self.chain.links[(source, destination)]

            for step in path:
                topo.update_link(
                    step[0],
                    step[1],
                    Link(topo.links[step].bandwidth + link.bandwidth),
                )
