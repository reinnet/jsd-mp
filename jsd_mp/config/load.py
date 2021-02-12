import os
import typing
import yaml

from domain import Chain, Type, Direction, Link, VNFM, Topology, Node
from .config import Config


def load(directory: str) -> Config:
    """
    load configuration files for:
    - physical toplogy (from topology.yml)
    - chains (from chains.yml)
    - vnf types (from types.yml)
    - vnfm (from vnfm.yml)
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
                    if entry.name == "topology.yml":
                        topology_yml = c
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
    topology = Topology()
    for n in topology_yml["nodes"]:
        d = Direction.NONE
        if n.get("ingress", False) and n.get("egress", False):
            d = Direction.BOTH
        elif n.get("egress", False):
            d = Direction.EGRESS
        elif n.get("ingress", False):
            d = Direction.INGRESS
        topology.add_node(
            n["id"],
            Node(
                cores=n["cores"],
                memory=n["ram"],
                vnf_support=n["vnfSupport"],
                direction=d,
                not_manager_nodes=n["notManagerNodes"],
            ),
        )
    for l in topology_yml["links"]:
        topology.add_link(
            l["source"], l["destination"], Link(bandwidth=l["bandwidth"])
        )

    return Config(types, chains, vnfm, topology)
