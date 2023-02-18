#!/usr/bin/env python3

"""
Find three nearest neighbors for each point

scripts/neighbors.py -s NC

For documentation, type:

scripts/neighbors.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

from baseline import *


### PARSE ARGUMENTS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Find three nearest neighbors for each point"
    )
    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-c", "--cycle", default=2020, help="The census cycle (e.g., 2020)", type=int
    )
    parser.add_argument(
        "-u",
        "--unit",
        default="block",
        help="The geographic unit (e.g., block)",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


class Pair(NamedTuple):
    one: int
    two: int

    def __repr__(self) -> str:
        return f"{self.one},{self.two}"


def main() -> None:
    """Find three nearest neighbors for each point

    Patterned after:
    https://stackoverflow.com/questions/61952561/how-do-i-find-the-neighbors-of-points-containing-coordinates-in-python
    """
    args: Namespace = parse_args()

    xx: str = args.state
    cycle: int = args.cycle
    unit: str = args.unit

    verbose: bool = args.verbose

    # Find the nearest neighbors for each point

    # Read the CSV
    rel_path: str = path_to_file(["data", xx]) + file_name(
        [xx, str(cycle), unit, "data"], "_", "csv"
    )
    df: pd.DataFrame = pd.read_csv(rel_path, sep=",")

    # Find the nearest neighbors for each point
    tree = BallTree(np.deg2rad(df[["Y", "X"]].values), metric="haversine")

    query_lats: pd.Series = df["Y"]
    query_lons: pd.Series = df["X"]
    # NOTE: k=4 because the first match is the point itself
    distances, indices = tree.query(np.deg2rad(np.c_[query_lats, query_lons]), k=4)

    graph: dict[str, list[str]] = {}
    neighbors: list[str, str] = list()

    r_km: int = 6371  # multiplier to convert to km (from unit distance)
    for geoid, d, ind in zip(df["GEOID"], distances, indices):
        graph[geoid] = []
        for i, index in enumerate(ind):
            if i == 0:
                # Skip the first match, which is the point itself
                continue
            graph[geoid].append(df["GEOID"][index])
            neighbors.append(Pair(geoid, df["GEOID"][index]))

    # Save the neighbors

    rel_path: str = path_to_file(["data", xx]) + file_name(
        [xx, str(cycle), unit, "pairs"], "_", "csv"
    )
    abs_path: str = FileSpec(rel_path).abs_path

    with open(abs_path, "w") as f:
        for i, pair in enumerate(neighbors):
            print(pair, file=f)

    pass


if __name__ == "__main__":
    main()

### END ###
