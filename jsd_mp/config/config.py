import dataclasses
import typing

from domain import Chain, Type, VNFM, Topology


@dataclasses.dataclass(frozen=True)
class Config:
    """
    Configurations of JSD-MP problem.
    These configurations try to be as general as possible.
    """

    types: typing.Dict[str, Type]
    chains: typing.List[Chain]
    vnfm: VNFM
    topology: Topology
