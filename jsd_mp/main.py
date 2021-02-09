"""
Entry point for JSD-MP (Joint Service Deployment - Manager Placement)
Here you can run solvers of this package on your network requests.
"""

import logging
import time
from typing import List, Tuple
from multiprocessing import Pool
import click

from result import Result, report_csv
from domain import Placement, ManagementPlacement
from config import load, Config


def execute(
    run: int,
    name: str,
    options: List[Tuple[str, str]],
    cfg: Config,
) -> Tuple[Result, List[Tuple[Placement, ManagementPlacement]]]:
    """
    Execute a solver run into isolated process to improve performance
    """
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

    return (
        Result(
            run=run,
            solver=name,
            elapsed_time=end - start,
            profit=solver.profit,
            cost=solver.cost,
            number_of_chains=len(cfg.chains),
            number_of_placed_chains=len(solver.solution),
        ),
        solver.solution,
    )


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
    type=click.Choice(["bari", "abu", "rari", "oabu"]),
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
    async_results = []

    with Pool() as pool:
        for run in range(runs):
            for name in solvers:
                async_result = pool.apply_async(
                    execute,
                    [
                        run,
                        name,
                        options,
                        cfg,
                    ],
                )
                async_results.append(async_result)

        for async_result in async_results:
            result, solution = async_result.get()

            print()
            print(f"{' run {} '.format(result.run + 1):*^50}")
            print()

            print(
                f"{result.name} solution takes {result.elapsed_time} seconds"
            )

            if show_placement is True:
                for (placement, manager_placement) in solution:
                    print(f"{placement.chain.name:=^25}")
                    print(placement)
                    print(manager_placement)
                print()

            print(
                f"Placement has profit: {result.profit} and cost: {result.cost}"
            )
            print(
                f"{len(solution)} has been placed"
                f" successfully from {len(cfg.chains)}"
            )

            results.append(result)

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
