#!/usr/bin/env python3

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/baseline_state.py -s NC -v > logs/NC_2020_congress_log.txt
$ scripts/baseline_state.py -s MD -v > logs/MD_2020_congress_log.txt
$ scripts/baseline_state.py -s PA -v > logs/PA_2020_congress_log.txt
$ scripts/baseline_state.py -s VA -v > logs/VA_2020_congress_log.txt

$ scripts/baseline_state.py -s OR -g -v > logs/OR_2020_congress_log.txt
$ scripts/baseline_state.py -s CA -t -v > logs/CA_2020_congress_log.txt

For documentation, type:

$ scripts/baseline_state.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any

from baseline import *


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
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Find districts that minimize population compactness."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = args.map

    verbose: bool = args.verbose

    #

    print()
    print(f"Generating a baseline map for {xx}/{plan_type}:")

    map_label: str = label_map(xx, plan_type)  # e.g., "NC20C"
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]

    input_csv: str = full_path([data_dir, xx], [xx, cycle, "vtd", "data"])
    pairs_csv = full_path([data_dir, xx], [xx, cycle, "vtd", "pairs"])
    output_csv: str = full_path([maps_dir], [map_label, "vtd", "assignments"])

    start: int = K * N * int(fips)
    iterations: int = 100

    # for i, seed in enumerate(range(start, start + iterations)):
    #     iter_label: str = label_iteration(i, K, N)
    #     print(f"... Iteration: {iter_label}, seed: {seed} ...")

    i: int = 0
    iter_label: str = label_iteration(i, K, N)

    # script args

    tmpdir: str = intermediate_dir + "/" + xx  # --tmpdir=./testing/tmp \
    N = N  # --N=6 \
    seed: int = start  # --seed=0 \
    prefix: str = map_label  # --prefix=file \ # TODO - Add iteration #
    data: str = input_csv  # --data=data.csv \
    adjacencies: str = pairs_csv  # --adjacencies=adjacent.csv \
    output: str = output_csv  # --output=output.csv

    do_baseline_run(tmpdir, N, seed, prefix, data, adjacencies, output, verbose)

    pass


if __name__ == "__main__":
    main()

### END ###
