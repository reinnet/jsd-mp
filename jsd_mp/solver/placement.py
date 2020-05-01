from __future__ import annotations

import dataclasses
import typing
import copy

from domain import Topology, Chain, Placement


@dataclasses.dataclass(frozen=True)
class PartialPlacement(Placement):
    def __init__(self, chain: Chain):
        super().__init__(chain=chain, nodes=[], links={})

    def __post_init__(self):
        pass

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

        super().apply_on_topology(topo)

        return topo
