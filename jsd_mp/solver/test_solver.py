import random
from unittest.mock import patch

from domain import (
    Type,
    Node,
    Topology,
    Link,
    Chain,
    VNFM,
)
from config import Config
from .random import Random
from .solver import Solver


class MockSolver(Solver):
    def _solve(self):
        return None


class TestSolver:
    def test_management_resource_availability_1(self):
        topo = Topology()
        topo.add_node("s1", Node(2, 2))
        topo.add_node("s2", Node(2, 2))
        topo.add_node("s3", Node(2, 2))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s1", Link(20))
        topo.add_link("s3", "s1", Link(20))
        topo.add_link("s3", "s2", Link(20))

        vnfm = VNFM(
            cores=2,
            radius=2,
            memory=2,
            bandwidth=2,
            license_cost=2,
            capacity=2,
        )

        cfg = Config(types={}, chains=[], topology=topo, vnfm=vnfm)

        solver = MockSolver(cfg)
        assert (
            solver.is_management_resource_available(
                topology=cfg.topology,
                manager="s3",
                nodes=["s1", "s2"],
            )
            is True
        )

    def test_management_resource_availability_2(self):
        topo = Topology()
        topo.add_node("s1", Node(2, 2))
        topo.add_node("s2", Node(2, 2, not_manager_nodes=["s3"]))
        topo.add_node("s3", Node(2, 2))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s1", Link(20))
        topo.add_link("s3", "s1", Link(20))
        topo.add_link("s3", "s2", Link(20))

        vnfm = VNFM(
            cores=2,
            radius=2,
            memory=2,
            bandwidth=2,
            license_cost=2,
            capacity=2,
        )

        cfg = Config(types={}, chains=[], topology=topo, vnfm=vnfm)

        solver = MockSolver(cfg)
        # reject with not_manager_nodes constraint
        assert (
            solver.is_management_resource_available(
                topology=cfg.topology,
                manager="s3",
                nodes=["s1", "s2"],
            )
            is False
        )

    def test_management_resource_availability_3(self):
        topo = Topology()
        topo.add_node("s1", Node(2, 2))
        topo.add_node("s2", Node(2, 2))
        topo.add_node("s3", Node(2, 2))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s3", Link(20))

        vnfm = VNFM(
            cores=2,
            radius=1,
            memory=2,
            bandwidth=2,
            license_cost=2,
            capacity=2,
        )

        cfg = Config(types={}, chains=[], topology=topo, vnfm=vnfm)

        # reject with radius
        solver = MockSolver(cfg)
        assert (
            solver.is_management_resource_available(
                topology=cfg.topology,
                manager="s1",
                nodes=["s2", "s3"],
            )
            is False
        )


class TestRandomSolver:
    def test_not_available_resources(self):
        fw = Type("fw", 2, 2)

        ch = Chain("ch-1", 100)

        ch.add_function(fw)
        ch.add_function(fw)
        ch.add_function(fw)
        ch.add_function(fw)

        ch.add_link(0, 1, Link(10))
        ch.add_link(1, 2, Link(10))
        ch.add_link(2, 3, Link(10))

        topo = Topology()
        topo.add_node("s1", Node(2, 2))
        topo.add_node("s2", Node(2, 2))
        topo.add_node("s3", Node(2, 2))
        topo.add_link("s1", "s2", Link(20))
        topo.add_link("s2", "s1", Link(20))
        topo.add_link("s3", "s1", Link(20))
        topo.add_link("s3", "s2", Link(20))

        vnfm = VNFM(2, 2, 2, 2, 2, 2)

        cfg = Config(types={"fw": fw}, chains=[ch], topology=topo, vnfm=vnfm)

        random.seed(a=1378)
        pls = Random(cfg).solve()

        assert len(pls) == 0

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

        cfg = Config(types={"fw": fw}, chains=[ch], topology=topo, vnfm=vnfm)

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
