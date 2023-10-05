#!/usr/bin/env python3

"""
Compare all the iteration maps with the one with the lowest energy.

For example:

$ scripts/compare_maps.py -s NC -i 100 -v

For documentation, type:

$ scripts/compare_maps.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

import csv
import itertools
import collections
import networkx as nx

from baseline.constants import (
    cycle,
    data_dir,
    intermediate_dir,
    maps_dir,
    districts_by_state,
    STATE_FIPS,
    study_unit,
)
from baseline.readwrite import file_name, path_to_file, read_csv, write_csv
from baseline.compare import cull_energies, find_best_plan
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
        help="The # of iterations to run (default: 100).",
        type=int,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def read_populations(populations_file: str) -> dict[str, int]:
    populations: dict[str, int] = {}
    with open(populations_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            populations[row["GEOID"]] = int(row["POP"])
    return populations


def read_plan(name: str, plan_file: str) -> dict:
    """Read a precinct-assignment file."""

    types: list = [str, int]
    precinct_assignments: list = read_csv(plan_file, types)  # A list of dicts

    plan: dict = dict()
    for assignment in precinct_assignments:
        plan[assignment["GEOID"]] = assignment["DISTRICT"]

    return {"name": name, "plan": plan}


def calc_edit_distance(plan1: dict, plan2: dict, populations: dict[str, int]) -> float:
    """Calculate the edit distance between two plans."""

    xname: str = plan1["name"]
    yname: str = plan2["name"]

    if xname == yname:
        return 0.0

    overlap_populations: dict[tuple[str, str], int] = collections.defaultdict(int)
    xmap: dict[str, str] = plan1["plan"]
    ymap: dict[str, str] = plan2["plan"]

    # Cloned from Todd's ensemble / all_pairs() code

    for geoid in xmap.keys():
        overlap = (xmap[geoid], ymap[geoid])
        overlap_populations[overlap] += populations[geoid]

    G = nx.Graph()
    for node, population in overlap_populations.items():
        G.add_node(node, weight=population)  # type: ignore
    for node1, node2 in itertools.combinations(overlap_populations.keys(), 2):
        if node1[0] != node2[0] and node1[1] != node2[1]:
            G.add_edge(node1, node2)  # type: ignore

    clique = nx.algorithms.clique.max_weight_clique(G)  # type: ignore
    size = clique[1]

    # End

    total_pop = sum(populations.values())
    moved: int = total_pop - size

    edit_distance: float = moved / total_pop

    return edit_distance


def main() -> None:
    """Compare all the iteration maps with the one with the lowest energy."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = args.map
    iterations: int = args.iterations
    unit: str = study_unit(xx)

    verbose: bool = args.verbose

    # Constants

    map_label: str = label_map(xx, plan_type)
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]
    start: int = K * N * int(fips)

    # Load populations by precinct

    data_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "data"], "_", "csv"
    )
    populations = read_populations(data_path)

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

    # Find the lowest energy, contiguous map, with 'roughly equal' populations

    best_plan_name: str = find_best_plan(plan_energies)
    best_plan_csv: str = full_path(
        [intermediate_dir, xx], [best_plan_name, "vtd", "assignments"]
    )
    best_plan: dict = read_plan(best_plan_name, best_plan_csv)

    # Compare each candidate map to it

    plans: list[dict] = list()

    for i, seed in enumerate(range(start, start + iterations)):
        compare_plan_name: str = map_label + "_" + label_iteration(i, K, N)

        # Make sure the map exists

        if compare_plan_name not in plan_energies:
            # This baseline iteration failed. Skip it.
            continue

        # Load the plan

        iter_label: str = label_iteration(i, K, N)
        compare_plan_csv: str = full_path(
            [intermediate_dir, xx], [map_label, iter_label, "vtd", "assignments"]
        )
        compare_plan: dict = read_plan(compare_plan_name, compare_plan_csv)

        # Compare the two plans

        edit_distance: float = calc_edit_distance(best_plan, compare_plan, populations)

        # Add a row to the list of plans

        plan: dict = plan_energies[compare_plan_name]
        plan["EDIT_DISTANCE"] = edit_distance
        plan["#"] = i + 1

        plans.append(plan)

    # Sort the maps by energy

    plans = sorted(plans, key=lambda plan: plan["ENERGY"])

    # Write analysis to file

    candidates_csv: str = path_to_file([maps_dir, xx]) + file_name(
        [map_label, "candidates"], "_", "csv"
    )

    write_csv(
        candidates_csv,
        plans,
        [
            "#",
            "MAP",
            "CONTIGUOUS",
            "POPDEV",
            "ENERGY",
            "EDIT_DISTANCE",
        ],
        precision="{:.6f}",
    )

    pass


if __name__ == "__main__":
    main()

### END ###
