from typing import List, NamedTuple
import csv


class Result(NamedTuple):
    """
    Result stores one run result
    """

    run: int
    profit: int  # profit means the total fee of chains
    cost: int  # cost means the total fee of licenses
    number_of_placed_chains: int
    number_of_chains: int
    solver: str
    elapsed_time: float


def report_csv(results: List[Result]):
    """
    write the report of all runs into a csv file with report.csv name.
    """

    with open("report.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=Result._fields)

        writer.writeheader()
        for result in results:
            writer.writerow(result._asdict())
