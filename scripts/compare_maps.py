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

import statistics

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
        default=1000,
        help="The # of iterations to run (default: 1000).",
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
    plan_energies: list[dict] = cull_energies(
        log_txt, xx, plan_type
    )  # These will be in ascending seed order

    # Find the lowest energy maps

    lowest_energies: dict[str, float]
    lowest_plans: dict[str, str]
    lowest_plans, lowest_energies = find_lowest_energies(plan_energies)
    inv_lowest_plans = {v: k for k, v in lowest_plans.items()}

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

    # Compare each candidate map

    plans: list[dict] = list()
    start: int = K * N * int(fips)

    for i, seed in enumerate(range(start, start + iterations)):
        # Load the plan

        iter_label: str = label_iteration(i, K, N)
        alt_plan_csv: str = full_path(
            [intermediate_dir, xx], [map_label, iter_label, "vtd", "assignments"]
        )
        alt_plan: Plan = Plan(alt_plan_csv, pop_by_geoid)

        # Compare the two plans

        diff: PlanDiff = PlanDiff(baseline, alt_plan)
        avg_uncertainty: float = statistics.fmean(diff.uom_by_district)
        avg_splits: float = statistics.fmean(diff.es_by_district)

        # Add a row to the list of plans

        plan: dict = plan_energies[i]

        name: str = plan["MAP"]
        energy: float = plan["ENERGY"]
        delta: float = (energy - lowest_energy) / lowest_energy
        plan["DELTA"] = delta

        note: str = ""
        if name in inv_lowest_plans:
            note = f"Lowest: {inv_lowest_plans[name]}"  # TODO
        plan["NOTE"] = note

        plan["UOM"] = avg_uncertainty
        plan["ES"] = avg_splits

        plans.append(plan)

    # TODO - Write analysis to file

    pass

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
