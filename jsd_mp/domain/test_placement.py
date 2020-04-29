from .placement import Placement
from .nfv import Chain, Type
from .topology import Link

import pytest


class TestPlacement:
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

        Placement(ch, ["n1", "n1", "n1", "n1"], {(0, 1): [], (1, 2): [], (2, 3): [],})

        with pytest.raises(ValueError):
            Placement(ch, ["n1", "n1", "n1"], {(0, 1): [], (1, 2): [], (2, 3): [],})

        with pytest.raises(ValueError):
            Placement(ch, ["n1", "n1", "n1", "n1"], {(1, 2): [], (2, 3): [],})
