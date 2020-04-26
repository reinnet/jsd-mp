import os
import yaml
import typing

from domain import Chain


def load(directory: str) -> typing.List[Chain]:
    """
    load configuration files for:
    - physical toplogy (topology.yml)
    - chains (chains.yml)
    - vnf types (types.yml)
    - vnfm (vnfm.yml)
    """
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name in (
                "topology.yml",
                "chains.yml",
                "types.yml",
                "vnfm.yml",
            ):
                with open(entry.path, "r") as f:
                    c = yaml.load(f)
                    if entry.name == "chains.yml":
                        for index, ch in enumerate(c):
                            fee = ch["cost"]
                            chain = Chain(f"ch-{index}", fee)
                            print(chain)


if __name__ == "__main__":
    load("../../simulation/config")
