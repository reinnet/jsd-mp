from .solver import Solver
from domain import (
    Placement,
    ManagementPlacement,
    Type,
    Node,
    Topology,
    Link,
    Chain,
    VNFM,
)
from config import Config

import typing
import random


class DummySolver(Solver):
    def solve(self) -> typing.List[typing.Tuple[Placement, ManagementPlacement]]:
        placements: typing.List[typing.Tuple[Placement, ManagementPlacement]] = []

        for chain in self.chains:
            nodes = []
            links = {}
            for function in chain.functions:
                n = random.choice(list(self.topology.nodes.keys()))
                nodes.append(n)
            for (source, destination), link in chain.links.items():
                r = self.topology.path(
                    nodes[source], nodes[destination], link.bandwidth
                )
                if r is not None:
                    links[(source, destination)] = r
            placements.append((Placement(chain, nodes, links), None))

        return placements


class TestDummySolver:
    def test_simple_chain(self):
        fw = Type("fw", 2, 2)

        ch = Chain("ch-1", 100)

        ch.add_function(fw)
        ch.add_function(fw)
        ch.add_function(fw)

        ch.add_link(0, 1, Link(10))
        ch.add_link(1, 2, Link(10))

        topo = Topology()
        topo.add_node("s1", Node(2, 2))
        topo.add_node("s2", Node(2, 2))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s1", Link(20))

        vnfm = VNFM(2, 2, 2, 2, 2, 2)

        cfg = Config(types=[fw], chains=[ch], topology=topo, vnfm=vnfm)

        random.seed(a=1378)
        pls = DummySolver(cfg).solve()

        assert pls[0].chain == ch
        assert len(pls[0].nodes) == 3
        assert len(pls[0].links) == 2

        assert pls[0].nodes == ["s1", "s1", "s2"]
        assert pls[0].links == {
            (0, 1): [],
            (1, 2): [("s1", "s2")],
        }
