import dataclasses
import typing

from domain import Chain, Type, VNFM, Topology


@dataclasses.dataclass(frozen=True)
class Config:
    types: typing.Dict[str, Type]
    chains: typing.List[Chain]
    vnfm: VNFM
    topology: Topology
