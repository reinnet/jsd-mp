from .nfv import Chain

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
