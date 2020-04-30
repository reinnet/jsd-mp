from config import load
from bari import Bari

import click
import logging


@click.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True))
@click.option("--verbose", "-v", default=False, is_flag=True)
@click.option("--placement", "-p", default=False, is_flag=True)
def bari(config, verbose, placement):
    if verbose is True:
        logging.basicConfig(level=logging.INFO)

    cfg = load(config)
    b = Bari(cfg)
    b.solve()

    if placement is True:
        for (p, pm) in b.solution:
            print(f"{p.chain.name:=^25}")
            for i, n in enumerate(p.nodes):
                print(f"funcion-{i} [{p.chain.functions[i].name}] is placed on {n}")

            for (f, t), path in p.links.items():
                print(f"function-{f} -> function{t} is placed on the following links:")
                for (f, t) in path:
                    print(f"\t{f} -> {t}")
        print()

    print(f"Placement has profit: {b.profit} and cost: {b.cost}")
    print(f"{len(b.solution)} has been placed successfully from {len(cfg.chains)}")


if __name__ == "__main__":
    bari()
