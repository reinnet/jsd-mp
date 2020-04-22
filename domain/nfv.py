import typing

from .direction import Direction


class Type:
    def __init__(self, name, cores, memory, direction=Direction.NONE):
        self.name: str = name
        self.cores: int = cores
        self.memory: int = memory
        self.direction: Direction = direction


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
