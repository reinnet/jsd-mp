import typing
import dataclasses

from .direction import Direction


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


class Chain:
    def __init__(self, name, fee):
        self.name: str = name
        self.fee: int = fee
        self.functions: typing.Listp[Type] = []

    def add_function(self, function: Type):
        self.functions.append(function)

    def __len__(self):
        return len(self.functions)

    def __iter__(self):
        return enumerate(self.functions)
