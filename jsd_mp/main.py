"""
Entry point for JSD-MP (Joint Service Deployment - Manager Placement)
Here you can run solvers of this package on your network requests.
"""

import logging
import time
from typing import List
import click

from result import Result, report_csv
from config import load


@click.command()
@click.option(
    "--config",
    "-c",
    required=True,
    type=click.Path(exists=True),
    help="configuration folder",
)
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    help="set the logging level to info",
)
@click.option(
    "--placement",
    "-p",
    "show_placement",
    default=False,
    is_flag=True,
    help="print the placement of VNFs and VNFMs",
)
@click.option(
    "--solvers",
    "-ss",
    multiple=True,
    default=["bari"],
    help="the solver",
    type=click.Choice(["bari", "abu", "rari"]),
)
@click.option(
    "--runs",
    "-r",
    default=1,
    type=int,
    help="number of runs to have stronger "
    "results if there is a randomness in solver",
)
@click.option(
    "--options", type=(str, int), help="solver options", multiple=True
)
def main(config, verbose, show_placement, solvers, runs, options):
    if verbose is True:
        logging.basicConfig(level=logging.INFO)

    start = time.time()
    cfg = load(config)
    end = time.time()
    print(f"load configuration takes {end - start} seconds")

    results: List[Result] = []

    for run in range(runs):
        print()
        print(f"{' run {} '.format(run + 1):*^50}")
        print()
        for name in solvers:
            # import solver based on given name, for example in case of bari
            # we import Bari from bari package.
            solver = getattr(__import__(name), name.title())(cfg)

            # pass options to the solver.
            # please note that these options are class propeties
            # on solver.
            for option, value in options:
                setattr(solver, option, value)

            start = time.time()
            solver.solve()
            end = time.time()
            print(f"{name} solution takes {end - start} seconds")

            if show_placement is True:
                for (placement, manager_placement) in solver.solution:
                    print(f"{placement.chain.name:=^25}")
                    print(placement)
                    print(manager_placement)
                print()

            print(
                f"Placement has profit: {solver.profit} and cost: {solver.cost}"
            )
            print(
                f"{len(solver.solution)} has been placed"
                f" successfully from {len(cfg.chains)}"
            )
            results.append(
                Result(
                    run=run,
                    solver=name,
                    elapsed_time=end - start,
                    profit=solver.profit,
                    cost=solver.cost,
                    number_of_chains=len(cfg.chains),
                    number_of_placed_chains=len(solver.solution),
                )
            )
    report_csv(results)


if __name__ == "__main__":
    print(
        """
  ╔╗╔═══╗╔═══╗     ╔═╗╔═╗╔═══╗
  ║║║╔═╗║╚╗╔╗║     ║║╚╝║║║╔═╗║
  ║║║╚══╗ ║║║║     ║╔╗╔╗║║╚═╝║
╔╗║║╚══╗║ ║║║║╔═══╗║║║║║║║╔══╝
║╚╝║║╚═╝║╔╝╚╝║╚═══╝║║║║║║║║
╚══╝╚═══╝╚═══╝     ╚╝╚╝╚╝╚╝

Joint Service Deployment - Manager Placement
Author: @1995parham (M.Sc. Thesis Summer 2019) with @bahador-bakhshi
            """
    )
    main()
