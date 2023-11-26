#!/usr/bin/env python3

"""
Score all the candidate baseline maps.

For example:

$ scripts/rebaseline_score_maps.py

For documentation, type:

$ scripts/rebaseline_score_maps.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

import os
from typing import Any

import rdadata as rdautils
import rdafn as rdafn

from baseline.constants import (
    cycle,
    # data_dir,
    # intermediate_dir,
    # maps_dir,
    districts_by_state,
    STATE_FIPS,
    study_unit,
)

# from baseline.readwrite import file_name, path_to_file, read_csv, write_csv
# from baseline.compare import cull_energies, find_best_plan
from baseline.baseline import label_map, label_iteration


def main() -> None:
    """Score all the candidate baseline maps."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = args.map
    iterations: int = args.iterations
    unit: str = study_unit(xx)
    original: bool = args.original

    verbose: bool = args.verbose

    #

    plan_dir: str = f"data/{xx}" if original else "rebaseline"
    maps_dir: str = f"maps/{xx}" if original else "rebaseline"
    qualifier: str = "_original" if original else "_rebaseline"

    map_label: str = label_map(xx, plan_type)
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]
    start: int = K * N * int(fips)

    ### SETUP FOR SCORING ###

    data_path: str = f"../rdadata/data/{xx}/{xx}_2020_data.csv"
    shapes_path: str = f"../rdadata/data/{xx}/{xx}_2020_shapes_simplified.json"
    graph_path: str = f"../rdadata/data/{xx}/{xx}_2020_graph.json"

    data: dict[str, dict[str, int]] = rdafn.load_data(data_path)
    shapes: dict[str, Any] = rdafn.load_shapes(shapes_path)
    graph: dict[str, list[str]] = rdafn.load_graph(graph_path)
    metadata: dict[str, Any] = rdafn.load_metadata(xx, data_path)

    scores: list[dict] = list()

    ### SCORE EACH CANDIDATE MAP ###

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)

        plan_name: str = map_label + "_" + iter_label + "_vtd_assignments.csv"
        plan_path: str = plan_dir + "/" + plan_name

        # Make sure the map exists

        if not os.path.exists(plan_path):
            continue

        # Load the plan & score it

        record: dict[str, Any] = dict()
        record["map"] = iter_label
        # record["energy"] = energy # TODO

        assignments: list[dict[str, str | int]] = rdafn.load_plan(plan_path)
        scorecard: dict[str, Any] = rdafn.analyze_plan(
            assignments,
            data,
            shapes,
            graph,
            metadata,
        )
        record.update(scorecard)
        scores.append(record)

    root_scores: str = maps_dir + "/" + f"{xx}_{cycle}_root_scores" + qualifier + ".csv"
    fields: list[str] = list(scores[0].keys())
    rdautils.write_csv(root_scores, scores, fields, precision="{:.6f}")


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
        "-o",
        "--original",
        dest="original",
        action="store_true",
        help="Original baseline maps (not rebaseline)",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


if __name__ == "__main__":
    main()

### END ###
