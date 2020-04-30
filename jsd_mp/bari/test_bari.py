from domain import Placement, Type, Node, Topology, Link, Chain, VNFM, Direction
from config import Config
from .bari import Bari


class TestBari:
    def test_complex_chain(self):
        fw = Type("fw", 2, 2)
        ingress = Type("in", 0, 0, Direction.INGRESS)
        egress = Type("out", 0, 0, Direction.EGRESS)
        svr = Type("svr", 2, 2)

        ch = Chain("ch", 100)

        ch.add_function(ingress)
        ch.add_function(fw)
        ch.add_function(svr)
        ch.add_function(egress)

        ch.add_link(0, 1, Link(10))
        ch.add_link(1, 2, Link(5))
        ch.add_link(2, 3, Link(5))

        topo = Topology()
        topo.add_node("s1", Node(2, 2))
        topo.add_node("s2", Node(2, 2, direction=Direction.NONE))
        topo.add_node("s3", Node(2, 2, direction=Direction.INGRESS))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s1", Link(20))
        topo.add_link("s1", "s3", Link(20))

        vnfm = VNFM(2, 2, 2, 2, 2, 2)

        cfg = Config(types=[fw], chains=[ch], topology=topo, vnfm=vnfm)

        bari = Bari(cfg)
        pls = bari.solve()

        assert len(pls) == 0

    def test_cost_of_chain(self):
        fw = Type("fw", 2, 2)

        ch1 = Chain("ch-1", 100)

        ch1.add_function(fw)
        ch1.add_function(fw)
        ch1.add_function(fw)

        ch1.add_link(0, 1, Link(10))
        ch1.add_link(1, 2, Link(10))

        ch2 = Chain("ch-2", 200)

        ch2.add_function(fw)
        ch2.add_function(fw)
        ch2.add_function(fw)

        ch2.add_link(0, 1, Link(10))
        ch2.add_link(1, 2, Link(10))

        topo = Topology()
        topo.add_node("s1", Node(2, 2))
        topo.add_node("s2", Node(2, 2))
        topo.add_node("s3", Node(2, 2))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s1", Link(20))
        topo.add_link("s1", "s3", Link(20))

        vnfm = VNFM(2, 2, 2, 2, 2, 2)

        cfg = Config(types=[fw], chains=[ch1, ch2], topology=topo, vnfm=vnfm)

        bari = Bari(cfg)
        pls = bari.solve()

        assert len(pls) == 1
        assert pls[0].chain.fee == 100

    def test_placeable_chain(self):
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
        topo.add_node("s3", Node(2, 2))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s1", Link(20))
        topo.add_link("s1", "s3", Link(20))

        vnfm = VNFM(2, 2, 2, 2, 2, 2)

        cfg = Config(types=[fw], chains=[ch], topology=topo, vnfm=vnfm)

        bari = Bari(cfg)
        pls = bari.solve()

        assert len(pls) == 1

        assert pls[0].nodes == ["s2", "s1", "s3"]
        assert pls[0].links == {
            (0, 1): [("s2", "s1")],
            (1, 2): [("s1", "s3")],
        }

        assert bari.topology.nodes["s1"].memory == 0
        assert bari.topology.nodes["s1"].cores == 0

        assert bari.topology.nodes["s2"].memory == 0
        assert bari.topology.nodes["s2"].cores == 0

        assert bari.topology.nodes["s3"].memory == 0
        assert bari.topology.nodes["s3"].cores == 0

    def test_not_placeable_chain(self):
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

        pls = Bari(cfg).solve()

        assert len(pls) == 0
