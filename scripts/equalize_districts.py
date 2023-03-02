#!/usr/bin/env python3
#

"""
Equalize district populations.

For example:

$ scripts/equalize_districts.py -s NC

For documentation, type:

$ scripts/equalize_districts.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from libpysal.weights import Rook
import random

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Equalize district populations."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Equalize district populations."""

    args: Namespace = parse_args()
    fips_map: dict[str, str] = make_state_codes()
    xx: str = args.state
    fips: str = fips_map[xx]

    unit: str = "vtd"

    verbose: bool = args.verbose

    # Load the precinct data

    data_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "data"], "_", "pickle"
    )
    features: list[Feature] = read_pickle(data_path)
    pop_by_geoid: dict[str, int] = {f["geoid"]: f["pop"] for f in features}
    del features

    # Load the unit (precinct) graph

    graph_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "graph"], "_", "pickle"
    )
    unit_graph: Rook = read_pickle(graph_path)

    # Load the precinct-assignment file

    uaf_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "assignments"], "_", "csv"
    )

    types: list = [str, int]
    assignments: list = read_typed_csv(uaf_path, types)

    district_by_geoid: dict[str, int] = dict()
    districts: dict[int, list] = dict()
    for row in assignments:
        district_by_geoid[row["GEOID20"]] = row["District"]
        if row["District"] not in districts:
            districts[row["District"]] = {
                "geoids": [],
                "population": 0,
                "border": [],
                "deviation": 0,
            }
        districts[row["District"]]["geoids"].append(row["GEOID20"])

    del assignments

    # Compute a district adjacency graph

    district_graph: dict[int, list[int]] = dict()
    for current, data in districts.items():
        neighbors: set[int] = set()

        for unit in data["geoids"]:
            for neighbor in unit_graph[unit]:
                other: int = district_by_geoid[neighbor]
                if other != current:
                    neighbors.add(other)

        district_graph[current] = list(neighbors)

    for id, data in districts.items():
        border: list[str] = id_border_units(
            id, data["geoids"], unit_graph, district_by_geoid
        )
        districts[id]["border"] = border

    # Compute the population balance point

    total_pop: int = sum(pop_by_geoid.values())
    n: int = len(districts)
    balance_point: int = total_pop // n

    # Compute the district populations

    for geoid, pop in pop_by_geoid.items():
        district: int = district_by_geoid[geoid]
        districts[district]["population"] += pop

    # Split precincts to equalize district populations

    for id in range(1, n + 1):
        districts[id]["deviation"] = districts[id]["population"] - balance_point

    split_graph: dict[
        int, list[int]
    ] = dict()  # Districts that can be equalized w/ each other
    for id, neighbors in district_graph.items():
        split_graph[id] = list()
        for neighbor in neighbors:
            x: int = districts[id]["deviation"]
            y: int = districts[neighbor]["deviation"]
            if abs(x) + abs(y) != abs(x + y):
                split_graph[id].append(neighbor)

    ## TODO - Figure out district-to-district splits

    i: int = 1
    while True:
        print(f"Attempt {i}")

        equalized: set(int) = set()
        mods: list = list()
        deviations: dict[int, list] = {k: v["deviation"] for k, v in districts.items()}

        fan_out: int = max([len(x) for x in split_graph.values()])
        for j in range(1, fan_out + 1):  # Start w/ the fewest options
            for from_id, neighbors in split_graph.items():  # Ignore equalized districts
                if from_id not in equalized and len(neighbors) == j:
                    to_id: int = neighbors[
                        random.randint(0, len(neighbors) - 1)
                    ]  # Randomly pick a neighbor

                    adjustment: int = deviations[from_id] * -1
                    deviations[from_id] += adjustment
                    deviations[to_id] -= adjustment

                    mod: dict = {"from": from_id, "to": to_id, "adjustment": adjustment}
                    mods.append(mod)

                    equalized.add(id)

        if sum(deviations.values()) == 0:
            break

        i += 1

    ## TODO - Translate district splits into precinct splits

    pass  # TODO


if __name__ == "__main__":
    main()

### END ###
