import os
import yaml
import typing
import dataclasses

from jsd_mp.domain import Chain, Type, Direction, Link, VNFM


@dataclasses.dataclass(frozen=True)
class Config:
    types: typing.Dict[str, Type]
    chains: typing.List[Chain]
    vnfm: VNFM


def load(directory: str) -> Config:
    """
    load configuration files for:
    - physical toplogy (topology.yml)
    - chains (chains.yml)
    - vnf types (types.yml)
    - vnfm (vnfm.yml)
    """
    types: typing.Dict[str, Type] = {}
    chains: typing.List[Chain] = []

    topology_yml = {}
    chains_yml = {}
    types_yml = {}
    vnfm_yml = {}

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name in (
                "topology.yml",
                "chains.yml",
                "types.yml",
                "vnfm.yml",
            ):
                with open(entry.path, "r") as f:
                    c = yaml.load(f, Loader=yaml.Loader)
                    if entry.name == "chains.yml":
                        chains_yml = c["chains"]
                    if entry.name == "types.yml":
                        types_yml = c["types"]
                    if entry.name == "vnfm.yml":
                        vnfm_yml = c
    # build structure from loaded yamls
    for t in types_yml:
        types[t["name"]] = Type(
            name=t["name"],
            cores=t["cores"],
            memory=t["ram"],
            # setup type direction
            direction=Direction.INGRESS
            if t.get("ingress", False)
            else Direction.EGRESS
            if t.get("egress", False)
            else Direction.NONE,
            manageable=t.get("manageable", True),
        )
    for i, c in enumerate(chains_yml):
        chain = Chain(name=f"ch-{i}", fee=c["cost"])
        for n in c["nodes"]:
            if n["type"] not in types:
                raise ValueError(f"{n['type']} is not a registered type")
            chain.add_function(types[n["type"]])
        for l in c["links"]:
            chain.add_link(l["source"], l["destination"], Link(l["bandwidth"]))

        chains.append(chain)
    vnfm = VNFM(
        cores=vnfm_yml["cores"],
        memory=vnfm_yml["ram"],
        capacity=vnfm_yml["capacity"],
        bandwidth=vnfm_yml["bandwidth"],
        radius=vnfm_yml["radius"],
        license_cost=vnfm_yml["licenseFee"],
    )

    return Config(types, chains, vnfm)
