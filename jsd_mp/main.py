from config import load
from bari import Bari

import click
import logging
import time


@click.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True))
@click.option("--verbose", "-v", default=False, is_flag=True)
@click.option("--placement", "-p", default=False, is_flag=True)
def bari(config, verbose, placement):
    if verbose is True:
        logging.basicConfig(level=logging.INFO)

    start = time.time()
    cfg = load(config)
    end = time.time()
    print(f"load configuration takes {end - start} seconds")

    b = Bari(cfg)
    start = time.time()
    b.solve()
    end = time.time()
    print(f"bari solution takes {end - start} seconds")

    if placement is True:
        for (p, pm) in b.solution:
            print(f"{p.chain.name:=^25}")
            for i, n in enumerate(p.nodes):
                print(f"funcion-{i} [{p.chain.functions[i].name}] is placed on {n}")

            for (f, t), path in p.links.items():
                print(f"function-{f} -> function-{t} is placed on the following links:")
                for (f, t) in path:
                    print(f"\t{f} -> {t}")

            print(f"manage by {pm.management_node}")

            for i, path in enumerate(pm.management_links):
                print(f"management route of function-{i}:")
                for (f, t) in path:
                    print(f"\t{f} -> {t}")
        print()

    print(f"Placement has profit: {b.profit} and cost: {b.cost}")
    print(f"{len(b.solution)} has been placed successfully from {len(cfg.chains)}")


if __name__ == "__main__":
    bari()
