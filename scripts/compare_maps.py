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

from collections import defaultdict

from baseline.constants import (
    cycle,
    temp_dir,
    intermediate_dir,
    districts_by_state,
    STATE_FIPS,
)
from baseline.readwrite import file_name, path_to_file, read_csv
from baseline.data import FeatureCollection
from baseline.compare import cull_energies
from baseline.baseline import label_map, full_path


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

    data_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "data"], "_", "pickle"
    )
    fc: FeatureCollection = FeatureCollection(data_path)

    # TODO - Pull the energies from the log file

    log_txt: str = full_path(
        [intermediate_dir, xx], [map_label, "log", str(iterations)], "txt"
    )
    plans: list[dict] = cull_energies(log_txt, xx, plan_type)

    # TODO

    lowest_map: str = "I536K01N14"

    # TODO - Load the lowest energy map

    lowest_map_csv: str = full_path(
        [intermediate_dir, xx], [map_label, lowest_map, "vtd", "assignments"]
    )
    assignments: list[dict[str, int]] = read_csv(lowest_map_csv, [str, int])
    _district_by_geoid: dict[str, int] = {
        str(d["GEOID"]): d["DISTRICT"] for d in assignments
    }
    del assignments

    # TODO - Invert it

    _geoids_by_district: dict[int, set[str]] = defaultdict(set)
    for geoid, district in _district_by_geoid.items():
        _geoids_by_district[district].add(geoid)

    # TODO - Calculate population by district

    # _pop_by_district: dict[int, int] = defaultdict(int)
    # for district, geoids in _geoids_by_district.items():
    #     for geoid in geoids:
    #         _pop_by_district[district] += pop_by_geoid[geoid]

    # TODO - Load each candidate map

    # TODO - Invert it

    # TODO - Compare the two

    pass


if __name__ == "__main__":
    main()

### END ###
