#!/usr/bin/env python3

"""
Score all the candidate baseline maps.

For example:

$ scripts/rebaseline_score_maps.py -s NC
$ scripts/rebaseline_score_maps.py -s NC -o

For documentation, type:

$ scripts/rebaseline_score_maps.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

import os
import csv
from collections import defaultdict
from typing import Any, List, NamedTuple, Dict

import rdadata as rdautils
import rdafn as rdafn

from baseline.constants import (
    cycle,
    districts_by_state,
    STATE_FIPS,
    study_unit,
)
from baseline.baseline import label_map, label_iteration


### HELPERS - Cloned from `rootmap` & lightly edited ###


class LatLong(NamedTuple):
    lat: float
    long: float


class Point(NamedTuple):
    geoid: str
    pop: float
    ll: LatLong


class Assignment(NamedTuple):
    geoid: str
    district: int


def read_redistricting_points(input: str) -> List[Point]:
    # read GEOID, POP, X, Y from CSV
    red_points: List[Point] = []
    with open(input, "r") as f:
        reader = csv.DictReader(f)
        geoid = ""
        for row in reader:
            if not geoid:
                geoid = "GEOID"
            red_point: Point = Point(
                geoid=row[geoid],
                pop=float(row["POP"]),
                ll=LatLong(
                    long=float(row["X"]),
                    lat=float(row["Y"]),
                ),
            )
            red_points.append(red_point)
    return red_points


def squared_distance(a: LatLong, b: LatLong) -> float:
    return (a.lat - b.lat) * (a.lat - b.lat) + (a.long - b.long) * (a.long - b.long)


def get_centroids(assigns: List[Assignment], points: Dict[str, Point]) -> list[LatLong]:
    bysite: defaultdict[int, List[Assignment]] = defaultdict(list)
    for a in assigns:
        bysite[a.district].append(a)
    cs: List[LatLong] = []
    top: int = max(s for s in bysite.keys())
    for site in range(1, top + 1):
        persite: List[Assignment] = bysite[site]
        total: float = sum(points[a.geoid].pop for a in persite)
        lat: float = (
            sum(points[a.geoid].ll.lat * points[a.geoid].pop for a in persite) / total
        )
        long: float = (
            sum(points[a.geoid].ll.long * points[a.geoid].pop for a in persite) / total
        )
        cs.append(LatLong(lat, long))
    return cs


def calc_energy(assignments: List[Assignment], points: Dict[str, Point]) -> float:
    """Calculate the energy of a map."""

    sites: List[LatLong] = get_centroids(assignments, points)
    total: float = sum(
        points[a.geoid].pop
        * squared_distance(
            sites[a.district - 1], points[a.geoid].ll
        )  # not sqrt!!! moment of inertia!
        for a in assignments
    )

    return total


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

    plan_dir: str = f"intermediate/{xx}" if original else "rebaseline"
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

    # For calculating energy

    points_csv: str = f"data/{xx}/{xx}_2020_vtd_data.csv"
    points_list: List[Point] = read_redistricting_points(points_csv)
    points: Dict[str, Point] = {p.geoid: p for p in points_list}

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

        plan: list[dict[str, str | int]] = rdafn.load_plan(plan_path)
        assignments: List[Assignment] = [
            Assignment(str(a["GEOID"]), int(a["DISTRICT"])) for a in plan
        ]
        energy: float = calc_energy(assignments, points)
        record["energy"] = energy

        scorecard: dict[str, Any] = rdafn.analyze_plan(
            plan,
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
