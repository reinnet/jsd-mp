import typing
import dataclasses

from .direction import Direction
from .topology import Link


@dataclasses.dataclass
class Type:
    """
    Each network function has a type with its specific requirements.
    This class describes theses requirements.
    """

    name: str
    cores: int
    memory: int
    direction: Direction = Direction.NONE
    manageable: bool = True


class Chain:
    def __init__(self, name, fee):
        self.name: str = name
        self.fee: int = fee
        self.functions: typing.List[Type] = []
        # stores connections in adjacency list
        self.connections: typing.Map(int, typing.List[int]) = {}
        # stores link information of source and destination
        self.links: typing.Map(typing.Tuple(int, int), Link) = {}

    def add_function(self, function: Type):
        self.functions.append(function)

    def add_link(self, source: int, destination: int, link: Link):
        if source < 0 or source >= len(self.functions):
            raise ValueError("source must be a valid index of a chain's function")
        if destination < 0 or destination >= len(self.functions):
            raise ValueError("destination must be a valid index of a chain's function")
        self.connections[source].append(destination)
        self.links[(source, destination)] = link

    def __len__(self):
        return len(self.functions)

    def __iter__(self):
        return enumerate(self.functions)
