#!/usr/bin/env python3

"""
Compare all the iteration maps with the one with the lowest energy.

For example:

$ scripts/compare_maps.py -s NC -i 1000 -v

For documentation, type:

$ scripts/compare_maps.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline.constants import (
    cycle,
    data_dir,
    intermediate_dir,
    districts_by_state,
    STATE_FIPS,
)
from baseline.readwrite import file_name, path_to_file, read_csv
from baseline.datatypes import Plan
from baseline.compare import cull_energies, find_lowest_energies, PlanDiff
from baseline.baseline import label_map, full_path, label_iteration


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Find districts that minimize population compactness."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
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
        help="The # of iterations to run (default: 10).",
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

    # Load the feature data

    data_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "data"], "_", "csv"
    )
    data: list[dict] = read_csv(data_path, [str, int, float, float])
    pop_by_geoid: dict[str, int] = {row["GEOID"]: row["POP"] for row in data}

    # Pull the energies from the log file

    log_txt: str = full_path(
        [intermediate_dir, xx], [map_label, "log", str(iterations)], "txt"
    )
    plans: list[dict] = cull_energies(log_txt, xx, plan_type)

    # Find the lowest energy maps

    lowest_energies: dict[str, float]
    lowest_plans: dict[str, str]
    lowest_plans, lowest_energies = find_lowest_energies(plans)

    lowest_energy: float = min(lowest_energies.values())
    lowest_plan: str = [
        lowest_plans[key]
        for key in lowest_energies
        if lowest_energies[key] == lowest_energy
    ][0]

    # Load the lowest energy map

    lowest_plan_csv: str = full_path(
        [intermediate_dir, xx], [map_label, lowest_plan, "vtd", "assignments"]
    )
    baseline: Plan = Plan(lowest_plan_csv, pop_by_geoid)

    # Load each candidate map

    start: int = K * N * int(fips)

    # Iterate creating baseline maps

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)
        alt_plan_csv: str = full_path(
            [intermediate_dir, xx], [map_label, iter_label, "vtd", "assignments"]
        )
        alt_plan: Plan = Plan(alt_plan_csv, pop_by_geoid)

        # TODO - Compare the two
        # TODO - Add to plans dict

        PlanDiff(baseline, alt_plan).splits
        avg_uncertainty: float
        avg_splits: float

        if i > 0:  # TODO - Remove
            break

    # TODO - Write analysis to file

    # energies_csv: str = full_path(
    #     [intermediate_dir, xx], [map_label, "energies", str(iterations)]
    # )

    # write_csv(
    #     energies_csv,
    #     maps,
    #     ["MAP", "ENERGY", "DELTA", "CONTIGUOUS", "NOTE"],
    #     precision="{:.6f}",
    # )

    pass


if __name__ == "__main__":
    main()

### END ###
