from .topology import Topology, Node, Link

import pytest
import copy


class TestTopology:
    def test_deep_copy(self):
        topo = Topology()

        topo.add_node("elahe", Node(1, 2))
        assert topo.nodes["elahe"].cores == 1
        assert topo.nodes["elahe"].memory == 2

        deep_topo = copy.deepcopy(topo)

        # deep copies of topology dom't change the base topology so they are GOOD
        deep_topo.update_node("elahe", Node(2, 2))

        assert topo.nodes["elahe"].cores == 1
        assert topo.nodes["elahe"].memory == 2

        assert deep_topo.nodes["elahe"].cores == 2
        assert deep_topo.nodes["elahe"].memory == 2

        # shallow copies of topology change the base topology so they are BAD
        shallow_topo = copy.copy(topo)

        shallow_topo.update_node("elahe", Node(2, 2))

        assert topo.nodes["elahe"].cores == 2
        assert topo.nodes["elahe"].memory == 2

        assert shallow_topo.nodes["elahe"].cores == 2
        assert shallow_topo.nodes["elahe"].memory == 2

    def test_unique_node_name(self):
        topo = Topology()

        topo.add_node("parham", Node(1, 2))
        with pytest.raises(ValueError):
            topo.add_node("parham", Node(1, 2))

    def test_invalid_link(self):
        topo = Topology()

        with pytest.raises(ValueError):
            topo.add_link("elahe", "parham", Link(10))

    def test_path(self):
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

        assert topo.path("s1", "s2", 5) == [("s1", "s2")]
        assert topo.path("s1", "s2", 15) is None
        assert topo.path("s1", "s3", 5) == [("s1", "s3")]
        assert topo.path("s1", "s3", 10) == [("s1", "s2"), ("s2", "s3")]

    def test_bfs(self):
        topo = Topology()

        topo.add_node("s1", Node(1, 2))
        topo.add_node("s2", Node(1, 2))
        topo.add_node("s3", Node(1, 2))
        topo.add_node("s4", Node(1, 2))
        topo.add_node("s5", Node(1, 2))

        topo.add_link("s1", "s2", Link(10))
        topo.add_link("s2", "s3", Link(10))
        topo.add_link("s3", "s4", Link(10))
        topo.add_link("s4", "s5", Link(5))

        assert topo.bfs("s1", 5) == [
            ("s1", 0),
            ("s2", 1),
            ("s3", 2),
            ("s4", 3),
            ("s5", 4),
        ]

        assert topo.bfs("s1", 10) == [
            ("s1", 0),
            ("s2", 1),
            ("s3", 2),
            ("s4", 3),
        ]

        with pytest.raises(ValueError):
            topo.bfs("s6", 10)

    def test_linear_topology(self):
        topo = Topology()

        assert hasattr(topo, "links")
        assert hasattr(topo, "connections")
        assert hasattr(topo, "nodes")

        topo.add_node("elahe", Node(8, 16))
        topo.add_node("parham", Node(1, 2))

        topo.add_link("elahe", "parham", Link(10))

        assert topo.connections["elahe"] == ["parham"]
        assert topo.connections["parham"] == []
