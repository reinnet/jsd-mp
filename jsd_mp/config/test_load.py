from .load import load
from domain import Direction


def test_laod():
    cfg = load("config_example")

    assert "ingress" in cfg.types
    assert cfg.types["ingress"].memory == 0
    assert cfg.types["ingress"].cores == 0
    assert cfg.types["ingress"].direction == Direction.INGRESS
    assert not cfg.types["ingress"].manageable

    assert len(cfg.chains) == 1
    assert cfg.chains[0].fee == 181
    assert cfg.chains[0].functions == [
        cfg.types["ingress"],
        cfg.types["vDPI"],
        cfg.types["vDPI"],
        cfg.types["vNAT"],
        cfg.types["egress"],
    ]

    assert cfg.vnfm.memory == 4
    assert cfg.vnfm.cores == 2
    assert cfg.vnfm.capacity == 10
    assert cfg.vnfm.radius == 100
    assert cfg.vnfm.bandwidth == 1
    assert cfg.vnfm.license_cost == 100

    assert "switch-15" in cfg.topology.nodes
    assert "server-1" in cfg.topology.nodes
    assert cfg.topology.nodes["server-1"].cores == 20
    assert cfg.topology.nodes["server-1"].memory == 100
    assert cfg.topology.nodes["server-1"].vnf_support
    assert cfg.topology.nodes["switch-9"].direction == Direction.BOTH
    assert "switch-12" in cfg.topology.connections["server-1"]
