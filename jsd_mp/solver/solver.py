from config import Config
from domain import Placement, ManagementPlacement

import abc
import typing
import copy


class Solver(abc.ABC):
    def __init__(self, config: Config):
        self.chains = config.chains
        self.vnfm = config.vnfm
        self.topology = copy.deepcopy(config.topology)

    @abc.abstractmethod
    def solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        pass
