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
    data: Rook = read_pickle(graph_path)
    unit_graph: Graph = Graph(data)
    # unit_graph: Rook = read_pickle(graph_path)

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

    graph_data: dict[int, list[int]] = dict()
    for current, data in districts.items():
        neighbors: set[int] = set()

        for geoid in data["geoids"]:
            for neighbor in unit_graph.neighbors(geoid):
                if neighbor == OUT_OF_STATE:
                    neighbors.add(OUT_OF_STATE)
                    continue

                other: int = district_by_geoid[neighbor]
                if other != current:
                    neighbors.add(other)

        graph_data[current] = list(neighbors)

    district_graph: Graph = Graph(graph_data)

    for id, data in districts.items():
        border: list[str] = border_shapes(
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

    ## Compute district-by-district deviations
    for id in range(1, n + 1):
        districts[id]["deviation"] = districts[id]["population"] - balance_point

    ## TODO - Figure out district-to-district splits
    # - Working outside in doesn't work: you can get islands
    # - Working across the districts ... ?

    equalized: set(int) = set()
    mods: list = list()
    deviations: dict[int, list] = {k: v["deviation"] for k, v in districts.items()}

    ## Find the starting point

    border: list = [OUT_OF_STATE]
    ring: list = district_graph.ring(border)

    data: dict[int, list[int]] = dict()
    for id, neighbors in district_graph.data().items():
        data[id] = list()
        for neighbor in neighbors:
            if neighbor == OUT_OF_STATE:
                continue
            x: int = districts[id]["deviation"]
            y: int = districts[neighbor]["deviation"]
            if abs(x) + abs(y) != abs(x + y):
                data[id].append(neighbor)

    split_graph: Graph = Graph(data)

    priority: list = [
        {
            "id": id,
            "options": len(split_graph.neighbors(id)),
            "deviation": deviations[id],
        }
        for id in ring
    ]
    priority = sorted(priority, key=lambda x: abs(x["deviation"]), reverse=True)
    priority = sorted(priority, key=lambda x: x["options"])
    priority = [district["id"] for district in priority]
    start: int = priority[0]
    next: set[int] = {start}

    while True:
        if len(next) == 0:
            break

        adjust: list[int] = list(next)

        for from_id in adjust:
            print(f"Equalize {from_id} ({districts[from_id]['deviation']})")

            candidates: set = (
                set(district_graph.neighbors(from_id, excluding=[OUT_OF_STATE]))
                - equalized
            )
            # candidates: set = set(split_graph.neighbors(from_id)) - equalized

            if len(candidates) == 1:
                # Only one candidate; use it
                to_id: int = candidates.pop()

            elif len(candidates) > 1:
                # More than one candidate
                to_id: int = None

                # Prioritize border districts
                for neighbor in candidates:
                    if district_graph.is_border(neighbor):
                        to_id = neighbor
                        break

                # Then pick a complementary one
                for neighbor in candidates:
                    x: int = districts[from_id]["deviation"]
                    y: int = districts[neighbor]["deviation"]
                    if abs(x) + abs(y) != abs(x + y):
                        to_id = neighbor
                        break

                # Failing those, pick one at random
                if to_id is None:
                    to_id = list(candidates)[random.randint(0, len(candidates) - 1)]

            else:
                raise Exception("No candidates")

            adjustment: int = deviations[from_id] * -1
            deviations[from_id] += adjustment
            deviations[to_id] -= adjustment

            mod: dict = {"from": from_id, "to": to_id, "adjustment": adjustment}
            mods.append(mod)

            equalized.add(from_id)

        next: set[int] = set()
        for id in equalized:
            next |= (
                set(district_graph.neighbors(id, excluding=[OUT_OF_STATE])) - equalized
            )
        # next: list[int] = set(split_graph.neighbors(from_id)) - equalized

        pass

    print(f"Done")

    pass  # TODO

    ## TODO - Translate district splits into precinct splits

    pass  # TODO


if __name__ == "__main__":
    main()

### END ###
