import os
import yaml
import typing

from jsd_mp.domain import Chain, Type, Direction, Link


def load(directory: str) -> typing.List[Chain]:
    """
    load configuration files for:
    - physical toplogy (topology.yml)
    - chains (chains.yml)
    - vnf types (types.yml)
    - vnfm (vnfm.yml)
    """
    types: typing.Dict[str, Type] = {}

    topology_yml = {}
    chains_yml = {}
    vnf_yml = {}
    vnfm_yml = {}

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name in (
                "topology.yaml",
                "chains.yaml",
                "types.yaml",
                "vnfm.yaml",
            ):
                with open(entry.path, "r") as f:
                    c = yaml.load(f, Loader=yaml.Loader)
                    if entry.name == "chains.yaml":
                        chains_yml = c["chains"]
                    if entry.name == "types.yaml":
                        types_yml = c["types"]
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
        )
    for i, c in enumerate(chains_yml):
        chain = Chain(name=f"ch-{i}", fee=c["cost"])
        for n in c["nodes"]:
            if n["type"] not in types:
                raise ValueError(f"{n['type']} is not a registered type")
            chain.add_function(types[n["type"]])
        for l in c["links"]:
            chain.add_link(l["source"], l["destination"], Link(l["bandwidth"]))


if __name__ == "__main__":
    load("../simulation/config")
