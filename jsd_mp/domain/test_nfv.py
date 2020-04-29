from .nfv import Chain, Type

import pytest
import dataclasses


class TestNFV:
    def test_chain(self):
        f1 = Type("fw", 1, 2)

        ch = Chain("elahe", 100)

        ch.add_function(f1)
        ch.add_function(f1)
        ch.add_function(f1)
        ch.add_function(f1)

        with pytest.raises(dataclasses.FrozenInstanceError):
            f1.cores = 2

        assert len(ch) == 4

        for (i, f), counter in zip(ch, range(len(ch))):
            assert f.name == "fw"
            assert i == counter
