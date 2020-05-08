from domain import Type, Node, Topology, Link, Chain, VNFM, Direction
from config import Config
from .abu import Abu


class TestAbu:
    def test_tree_topoloy(self):
        topo = Topology()
        topo.add_node("s0", Node(0, 0, direction=Direction.BOTH))
        topo.add_node("s1", Node(0, 0))
        topo.add_node("s2", Node(0, 0))
        for n in ("n1", "n2", "n3", "n4", "n5", "n6"):
            topo.add_node(n, Node(2, 2))
        topo.add_link("s0", "s1", Link(15))
        topo.add_link("s1", "s0", Link(15))
        topo.add_link("s0", "s2", Link(15))
        topo.add_link("s2", "s0", Link(15))
        for n in ("n1", "n2", "n3"):
            topo.add_link("s1", n, Link(15))
            topo.add_link(n, "s1", Link(15))
        for n in ("n4", "n5", "n6"):
            topo.add_link("s2", n, Link(15))
            topo.add_link(n, "s2", Link(15))

        fw = Type("fw", 2, 2)
        ingress = Type("in", 0, 0, Direction.INGRESS, False)
        egress = Type("out", 0, 0, Direction.EGRESS, False)
        svr = Type("svr", 2, 2)

        ch1 = Chain("ch-1", 100)
        ch1.add_function(ingress)
        ch1.add_function(fw)
        ch1.add_function(svr)
        ch1.add_function(egress)
        ch1.add_link(0, 1, Link(5))
        ch1.add_link(1, 2, Link(5))
        ch1.add_link(2, 3, Link(5))

        ch2 = Chain("ch-2", 200)
        ch2.add_function(ingress)
        ch2.add_function(fw)
        ch2.add_function(svr)
        ch2.add_function(egress)
        ch2.add_link(0, 1, Link(5))
        ch2.add_link(1, 2, Link(5))
        ch2.add_link(2, 3, Link(5))

        ch3 = Chain("ch-3", 300)
        ch3.add_function(ingress)
        ch3.add_function(fw)
        ch3.add_function(svr)
        ch3.add_function(egress)
        ch3.add_link(0, 1, Link(5))
        ch3.add_link(1, 2, Link(5))
        ch3.add_link(2, 3, Link(5))

        vnfm = VNFM(
            cores=2, memory=2, capacity=4, radius=100, bandwidth=1, license_cost=100
        )

        cfg = Config(types=[fw], chains=[ch1, ch2], topology=topo, vnfm=vnfm)

        abu = Abu(cfg)
        abu.solve()

        assert len(abu.solution) == 2
        assert abu.profit == 300

        cfg = Config(types=[fw], chains=[ch1, ch2, ch3], topology=topo, vnfm=vnfm)

        abu = Abu(cfg)
        abu.solve()

        assert len(abu.solution) == 0
