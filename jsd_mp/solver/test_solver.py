from .random import Random
from domain import (
    Type,
    Node,
    Topology,
    Link,
    Chain,
    VNFM,
)
from config import Config

import random


class TestRandomSolver:
    def test_simple_chain(self):
        fw = Type("fw", 2, 2)

        ch = Chain("ch-1", 100)

        ch.add_function(fw)
        ch.add_function(fw)

        ch.add_link(0, 1, Link(10))

        topo = Topology()
        topo.add_node("s1", Node(2, 2))
        topo.add_node("s2", Node(2, 2))
        topo.add_node("s3", Node(2, 2))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s1", Link(20))
        topo.add_link("s3", "s1", Link(20))
        topo.add_link("s3", "s2", Link(20))

        vnfm = VNFM(2, 2, 2, 2, 2, 2)

        cfg = Config(types=[fw], chains=[ch], topology=topo, vnfm=vnfm)

        random.seed(a=1378)
        pls = Random(cfg).solve()

        assert len(pls) == 1

        assert pls[0][0].chain == ch
        assert len(pls[0][0].nodes) == 2
        assert len(pls[0][0].links) == 1

        assert pls[0][0].nodes == ["s1", "s2"]
        assert pls[0][0].links == {
            (0, 1): [("s1", "s2")],
        }

        assert pls[0][1].management_node == "s3"
