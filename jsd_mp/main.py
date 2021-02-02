"""
Entry point for JSD-MP (Joint Service Deployment - Manager Placement)
Here you can run solvers of this package on your network requests.
"""

import logging
import time
import click

from config import load


@click.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True))
@click.option("--verbose", "-v", default=False, is_flag=True)
@click.option("--placement", "-p", default=False, is_flag=True)
@click.option("--solvers", "-ss", multiple=True, default=["bari"])
def main(config, verbose, placement, solvers):
    if verbose is True:
        logging.basicConfig(level=logging.INFO)

    start = time.time()
    cfg = load(config)
    end = time.time()
    print(f"load configuration takes {end - start} seconds")

    for name in solvers:
        solver = getattr(__import__(name), name.title())(cfg)

        start = time.time()
        solver.solve()
        end = time.time()
        print(f"{name} solution takes {end - start} seconds")

        if placement is True:
            for (p, pm) in solver.solution:
                print(f"{p.chain.name:=^25}")
                print(p)
                print(pm)
            print()

        print(f"Placement has profit: {solver.profit} and cost: {solver.cost}")
        print(
            f"{len(solver.solution)} has been placed"
            f" successfully from {len(cfg.chains)}"
        )


if __name__ == "__main__":
    print(
        """
  ╔╗╔═══╗╔═══╗     ╔═╗╔═╗╔═══╗
  ║║║╔═╗║╚╗╔╗║     ║║╚╝║║║╔═╗║
  ║║║╚══╗ ║║║║     ║╔╗╔╗║║╚═╝║
╔╗║║╚══╗║ ║║║║╔═══╗║║║║║║║╔══╝
║╚╝║║╚═╝║╔╝╚╝║╚═══╝║║║║║║║║
╚══╝╚═══╝╚═══╝     ╚╝╚╝╚╝╚╝

Author: @1995parham (M.Sc. Thesis Summer 2019)
            """
    )
    main()
