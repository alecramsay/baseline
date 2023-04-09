#!/usr/bin/env python3

"""
TODO - Derive a characteristic signature for each map.

For example:

$ scripts/signature.py -s NC -i 100 -v

For documentation, type:

$ scripts/signature.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

import statistics
import math

from baseline.constants import (
    cycle,
    data_dir,
    intermediate_dir,
    maps_dir,
    districts_by_state,
    STATE_FIPS,
)
from baseline.readwrite import file_name, path_to_file, read_csv, write_csv
from baseline.datatypes import Plan, Coordinate
from baseline.compare import cull_energies, find_lowest_energies, PlanDiff
from baseline.baseline import label_map, full_path, label_iteration


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Find districts that minimize population compactness."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="AZ",  # TODO - change to NC
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-m",
        "--map",
        default="congress",
        help="The type of map: { congress | upper | lower }.",
        type=str,
    )
    parser.add_argument(
        "-i",
        "--iterations",
        default=100,
        help="The # of iterations to run (default: 100).",
        type=int,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Compare all the iteration maps with the one with the lowest energy."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = args.map
    iterations: int = args.iterations
    unit: str = "vtd"  # Mod for CA & OR

    verbose: bool = args.verbose

    # Constants

    map_label: str = label_map(xx, plan_type)
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]
    start: int = K * N * int(fips)

    # Load the feature data

    data_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "data"], "_", "csv"
    )
    data: list[dict] = read_csv(
        data_path, [str, int, float, float]
    )  # <= GEOID, POP, X, Y
    pop_by_geoid: dict[str, int] = {row["GEOID"]: row["POP"] for row in data}

    # ADDED
    # Convert the list of dicts to a dict of dicts indexed by GEOID
    # Compute the bounding box for the state

    data_by_geoid: dict[str, dict] = {
        row["GEOID"]: {"POP": row["POP"], "X": row["X"], "Y": row["Y"]} for row in data
    }
    min_x: float = 180.0
    max_x: float = -180.0
    min_y: float = 90.0
    max_y: float = -90.0
    for row in data:
        if row["X"] < min_x:
            min_x = row["X"]
        if row["X"] > max_x:
            max_x = row["X"]
        if row["Y"] < min_y:
            min_y = row["Y"]
        if row["Y"] > max_y:
            max_y = row["Y"]

    center_of_state_bbox: Coordinate = Coordinate(
        (min_x + max_x) / 2.0, (min_y + max_y) / 2.0
    )

    # Pull the energies from the log file

    log_txt: str = full_path(
        [intermediate_dir, xx], [map_label, "log", str(iterations)], "txt"
    )
    plan_energies: dict[str, dict] = cull_energies(log_txt, xx, plan_type)

    if len(plan_energies) != iterations:
        print(f"Missing iterations: Expected {iterations}; got {len(plan_energies)}.")
        for i, seed in enumerate(range(start, start + iterations)):
            map_name: str = map_label + "_" + label_iteration(i, K, N)
            if map_name not in plan_energies:
                print(f"Map {map_name} not in log.")

    # Find the lowest energy maps

    lowest_energies: dict[str, float]
    lowest_plans: dict[str, str]
    lowest_plans, lowest_energies = find_lowest_energies(plan_energies)

    lowest_energy: float = min(lowest_energies.values())
    lowest_plan: str = [
        lowest_plans[key]
        for key in lowest_energies
        if lowest_energies[key] == lowest_energy
    ][0]

    ### DELETED ...

    for i, seed in enumerate(range(start, start + iterations)):
        map_name: str = map_label + "_" + label_iteration(i, K, N)

        # Make sure the map exists

        if map_name not in plan_energies:
            # This baseline iteration failed. Skip it.
            continue

        # Load the plan

        iter_label: str = label_iteration(i, K, N)
        alt_plan_csv: str = full_path(
            [intermediate_dir, xx], [map_label, iter_label, "vtd", "assignments"]
        )
        alt_plan: Plan = Plan(alt_plan_csv, pop_by_geoid)

        # ADDED
        # Compute a signature "distance" for each map

        centroids: list[Coordinate] = list()
        for district in alt_plan.district_ids:
            district_pop: int = alt_plan.population_for_district(district)

            temp_x: float = 0.0
            temp_y: float = 0.0
            for geoid in alt_plan.geoids_for_district(district):
                temp_x += data_by_geoid[geoid]["POP"] * data_by_geoid[geoid]["X"]
                temp_y += data_by_geoid[geoid]["POP"] * data_by_geoid[geoid]["Y"]

            centroids.append(Coordinate(temp_x / district_pop, temp_y / district_pop))

        avg_x: float = sum([x for x, y in centroids]) / len(centroids)
        avg_y: float = sum([y for x, y in centroids]) / len(centroids)
        center_of_districts: Coordinate = Coordinate(avg_x, avg_y)

        normalized_center: Coordinate = Coordinate(
            round((center_of_districts.x / center_of_state_bbox.x) * 1000, 3),
            round((center_of_districts.y / center_of_state_bbox.y) * 1000, 3),
        )

        print(f"Center for {map_name}: {normalized_center}")

        # for i, centroid in enumerate(centroids):
        #     print(f"Centroids for district {i + 1}: {centroid}")

        # district_distances: list[float] = list()
        # for centroid in centroids:
        #     d: float = math.sqrt(
        #         (centroid.x - center.x) ** 2 + (centroid.y - center.y) ** 2
        #     )
        #     district_distances.append(d)

        # # TODO - How should district distances be combined?

        # signature: float = sum(district_distances)

        # print(f"Signature for {map_name}: {signature}")

        pass

    pass


if __name__ == "__main__":
    main()

### END ###
