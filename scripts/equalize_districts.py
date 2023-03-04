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
from collections import defaultdict

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
    xx: str = args.state

    # fips_map: dict[str, str] = make_state_codes()
    # fips: str = fips_map[xx]

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
    data: dict = read_pickle(graph_path)
    unit_graph: Graph = Graph(data)

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

    ## Figure out district-to-district splits

    ### Prioritize the districts

    queue: list = [
        {
            "id": id,
            "options": len(district_graph.neighbors(id, excluding=[OUT_OF_STATE])),
            "deviation": districts[id]["deviation"],
        }
        for id in districts.keys()
    ]
    queue = sorted(queue, key=lambda x: abs(x["deviation"]), reverse=True)
    queue = sorted(queue, key=lambda x: x["options"])
    queue = [district["id"] for district in queue]

    ### Calculate the initial deviations & aggregate absolute deviation

    deviations: dict[int, list] = {k: v["deviation"] for k, v in districts.items()}
    discrepancy: int = sum(abs(v) for v in deviations.values())
    initial: int = discrepancy

    ### Swap population between adjacent districts, until the discrepancy is minimized

    i: int = 1
    j: int = 1
    mods: list = list()
    while discrepancy > n:  # +/- 1 person per district
        if verbose:
            print()
            print(f"Round {j} discrepancy: {discrepancy}")

        for from_id in queue:
            for to_id in district_graph.neighbors(from_id, excluding=[OUT_OF_STATE]):
                x: int = deviations[from_id]
                y: int = deviations[to_id]
                if (abs(x) + abs(y) != abs(x + y)) or (abs(x) > 0):
                    adjustment: int = deviations[from_id] * -1
                    deviations[from_id] += adjustment
                    deviations[to_id] -= adjustment

                    mod: dict = {
                        "i": i,
                        "from": from_id,
                        "to": to_id,
                        "adjustment": adjustment,
                    }
                    mods.append(mod)

                    if verbose:
                        print(f"  {from_id} -> {to_id}: {adjustment}")

                    i += 1

        discrepancy: int = sum(abs(v) for v in deviations.values())
        j += 1

    final: int = discrepancy

    if verbose:
        print()
        print(f"Initial: {initial} => final: {final}; # mods: {len(mods)}")

    ### Aggregate the modifications by district-district pair

    offsets: dict = defaultdict(int)
    for mod in mods:
        one: int
        two: int
        adjustment: int

        if mod["from"] < mod["to"]:
            one = mod["from"]
            two = mod["to"]
            adjustment = mod["adjustment"]
        else:
            one = mod["to"]
            two = mod["from"]
            adjustment = mod["adjustment"] * -1

        offsets[Pair(one, two)] += mod["adjustment"]

    if verbose:
        moved: int = sum(abs(v) for v in offsets.values())

        print()
        print(f"Moved: {moved} people between {len(offsets)} pairs:")
        for pair, adjustment in offsets.items():
            print(f"  {pair}: {adjustment}")
        print()

    pass  # TODO

    ## TODO - Translate district splits into precinct splits

    pass  # TODO


if __name__ == "__main__":
    main()

### END ###
