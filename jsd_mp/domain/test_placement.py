from .placement import Placement
from .nfv import Chain, Type
from .topology import Link, Node, Topology

import pytest


class TestPlacement:
    def test_apply_on_topology(self):
        topo = Topology()

        topo.add_node("s1", Node(1, 2))
        topo.add_node("s2", Node(1, 2))
        topo.add_node("s3", Node(1, 2))
        topo.add_node("s4", Node(1, 2))
        topo.add_node("s5", Node(1, 2))

        topo.add_link("s1", "s2", Link(10))
        topo.add_link("s1", "s3", Link(5))
        topo.add_link("s2", "s3", Link(10))
        topo.add_link("s3", "s4", Link(10))
        topo.add_link("s4", "s5", Link(5))

        f1 = Type("fw", 1, 2)

        ch = Chain("elahe", 100)

        ch.add_function(f1)
        ch.add_function(f1)
        ch.add_function(f1)
        ch.add_function(f1)

        ch.add_link(0, 1, Link(10))
        ch.add_link(1, 2, Link(10))
        ch.add_link(2, 3, Link(10))

        Placement(
            ch,
            ["s1", "s2", "s3", "s4"],
            {(0, 1): [("s1", "s2")], (1, 2): [("s2", "s3")], (2, 3): [("s3", "s4")]},
        ).apply_on_topology(topo)

        assert topo.nodes["s1"].memory == 0
        assert topo.nodes["s1"].cores == 0
        assert topo.nodes["s2"].memory == 0
        assert topo.nodes["s2"].cores == 0
        assert topo.nodes["s3"].memory == 0
        assert topo.nodes["s3"].cores == 0
        assert topo.nodes["s4"].memory == 0
        assert topo.nodes["s4"].cores == 0
        assert topo.nodes["s5"].memory == 2
        assert topo.nodes["s5"].cores == 1

        assert topo.links[("s1", "s2")].bandwidth == 0
        assert topo.links[("s2", "s3")].bandwidth == 0
        assert topo.links[("s3", "s4")].bandwidth == 0
        assert topo.links[("s1", "s3")].bandwidth == 5
        assert topo.links[("s4", "s5")].bandwidth == 5

    def test_revert_on_topology(self):
        topo = Topology()

        topo.add_node("s1", Node(0, 0))
        topo.add_node("s2", Node(0, 0))
        topo.add_node("s3", Node(0, 0))
        topo.add_node("s4", Node(0, 0))
        topo.add_node("s5", Node(1, 2))

        topo.add_link("s1", "s2", Link(0))
        topo.add_link("s1", "s3", Link(5))
        topo.add_link("s2", "s3", Link(0))
        topo.add_link("s3", "s4", Link(0))
        topo.add_link("s4", "s5", Link(5))

        f1 = Type("fw", 1, 2)

        ch = Chain("elahe", 100)

        ch.add_function(f1)
        ch.add_function(f1)
        ch.add_function(f1)
        ch.add_function(f1)

        ch.add_link(0, 1, Link(10))
        ch.add_link(1, 2, Link(10))
        ch.add_link(2, 3, Link(10))

        Placement(
            ch,
            ["s1", "s2", "s3", "s4"],
            {(0, 1): [("s1", "s2")], (1, 2): [("s2", "s3")], (2, 3): [("s3", "s4")]},
        ).revert_on_topology(topo)

        assert topo.nodes["s1"].memory == 2
        assert topo.nodes["s1"].cores == 1
        assert topo.nodes["s2"].memory == 2
        assert topo.nodes["s2"].cores == 1
        assert topo.nodes["s3"].memory == 2
        assert topo.nodes["s3"].cores == 1
        assert topo.nodes["s4"].memory == 2
        assert topo.nodes["s4"].cores == 1
        assert topo.nodes["s4"].memory == 2
        assert topo.nodes["s4"].cores == 1

        assert topo.links[("s1", "s2")].bandwidth == 10
        assert topo.links[("s2", "s3")].bandwidth == 10
        assert topo.links[("s3", "s4")].bandwidth == 10
        assert topo.links[("s1", "s3")].bandwidth == 5
        assert topo.links[("s4", "s5")].bandwidth == 5

    def test_single_chain_placement(self):
        f1 = Type("fw", 1, 2)

        ch = Chain("elahe", 100)

        ch.add_function(f1)
        ch.add_function(f1)
        ch.add_function(f1)
        ch.add_function(f1)

        ch.add_link(0, 1, Link(100))
        ch.add_link(1, 2, Link(100))
        ch.add_link(2, 3, Link(100))

        Placement(ch, ["n1", "n1", "n1", "n1"], {(0, 1): [], (1, 2): [], (2, 3): []})

        with pytest.raises(ValueError):
            Placement(ch, ["n1", "n1", "n1"], {(0, 1): [], (1, 2): [], (2, 3): []})

        with pytest.raises(ValueError):
            Placement(ch, ["n1", "n1", "n1", "n1"], {(1, 2): [], (2, 3): []})
