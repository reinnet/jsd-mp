"""
Entry point for JSD-MP (Joint Service Deployment - Manager Placement)
Here you can run solvers of this package on your network requests.
"""

import logging
import time
import click

from config import load
from bari import Bari


@click.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True))
@click.option("--verbose", "-v", default=False, is_flag=True)
@click.option("--placement", "-p", default=False, is_flag=True)
def bari(config, verbose, placement):
    """
    Bari command run the Bari solver.
    """
    if verbose is True:
        logging.basicConfig(level=logging.INFO)

    start = time.time()
    cfg = load(config)
    end = time.time()
    print(f"load configuration takes {end - start} seconds")

    solver = Bari(cfg)
    start = time.time()
    solver.solve()
    end = time.time()
    print(f"bari solution takes {end - start} seconds")

    if placement is True:
        for (p, pm) in solver.solution:
            print(f"{p.chain.name:=^25}")
            print(p)
            print(pm)
        print()

    print(f"Placement has profit: {solver.profit} and cost: {solver.cost}")
    print(f"{len(solver.solution)} has been placed successfully from {len(cfg.chains)}")


if __name__ == "__main__":
    bari()
