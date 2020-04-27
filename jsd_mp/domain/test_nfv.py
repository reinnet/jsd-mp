from .nfv import Chain, Type


class TestNFV:
    def test_chain(self):
        f1 = Type("fw", 1, 2)

        ch = Chain("elahe", 100)

        ch.add_function("1", f1)
        ch.add_function("2", f1)
        ch.add_function("3", f1)
        ch.add_function("3", f1)

        assert len(ch) == 4

        for (i, f), counter in zip(ch, range(len(ch))):
            assert f.name == "fw"
            assert i == counter
