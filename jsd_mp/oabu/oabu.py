import random
import itertools
import typing

from abu import Abu
from domain import (
    Placement,
    ManagementPlacement,
    Chain,
    Topology,
)


class Oabu(Abu):
    """
    Optimized Abu implements
    the Mohammad Abu-Lebdeh (10.1109/TNSM.2017.2730199)
    tabu search for placing the VNFMs but with some optimization
    to support our problem constraints.

    Please refer to Abu class for more information.
    """

    def place_manager(
        self, chain: Chain, topology: Topology, placement: Placement
    ) -> typing.Union[ManagementPlacement, None]:
        """
        selects manager from the chain's node then reserves bandwidth
        for its connections.
        if there isn't any node that can be vnfm from the chain we are going
        to randomly select another node.
        """
        node = ""

        # returns list of the physical nodes that runs manageable functions.
        # managable functions needs manager and placement only contains
        # the single chain placement.
        # we select one of these nodes as chain manager.
        for _node in set(
            itertools.compress(placement.nodes, chain.manageable_functions)
        ):
            if self.is_management_resource_available(
                topology,
                _node,
                list(
                    itertools.compress(
                        placement.nodes, chain.manageable_functions
                    )
                ),
            ):
                node = _node
                break
        else:
            # we cannot find any node from the chain that support vnfm
            # lets do some random selection similar
            # to what we are doing at tabu search
            for _ in range(self.n_iter):
                vnfm = random.choice(
                    list(
                        set(self.topology.nodes)
                        - set(
                            itertools.compress(
                                placement.nodes, chain.manageable_functions
                            )
                        )
                    )
                )
                if self.is_management_resource_available(
                    self.topology,
                    vnfm,
                    list(
                        itertools.compress(
                            placement.nodes, chain.manageable_functions
                        )
                    ),
                ):
                    node = vnfm
                    break
            else:
                return None

        paths = []
        for _node in itertools.compress(
            placement.nodes, placement.chain.manageable_functions
        ):
            path = topology.path(node, _node, self.vnfm.bandwidth)
            if path is not None:
                paths.append(path)

        return ManagementPlacement(chain, self.vnfm, node, paths)
