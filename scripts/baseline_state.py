#!/usr/bin/env python3

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/baseline_state.py -s NC -i 10 -v > intermediate/NC/NC20C_log_10.txt
$ scripts/baseline_state.py -s NC -i 100 -v > intermediate/NC/NC20C_log_100.txt
$ scripts/baseline_state.py -s NC -i 1000 -v > intermediate/NC/NC20C_log_1000.txt

For documentation, type:

$ scripts/baseline_state.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

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
        "-i",
        "--iterations",
        default=10,
        help="The # of iterations to run (default: 10).",
        type=int,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


@time_function
def main() -> None:
    """Find districts that minimize population compactness."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = args.map
    iterations: int = args.iterations

    verbose: bool = args.verbose

    # Add dccvt to the path

    path_list: list[str] = [
        "/Users/alecramsay/iCloud/dev/dccvt/examples/redistricting",
        "/Users/alecramsay/iCloud/dev/dccvt/bin",
    ]
    os.environ["PATH"] += os.pathsep + os.pathsep.join(path_list)

    # Set up

    print()
    print(f"Generating baseline maps for {xx}/{plan_type}:")

    map_label: str = label_map(xx, plan_type)  # e.g., "NC20C"
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]

    input_csv: str = full_path([data_dir, xx], [xx, cycle, "vtd", "data"])
    pairs_csv = full_path([data_dir, xx], [xx, cycle, "vtd", "pairs"])

    start: int = K * N * int(fips)

    # Iterate creating baseline maps

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)
        print()
        print(f"... Iteration: {iter_label}, seed: {seed} ...")

        output_csv: str = full_path(
            [intermediate_dir, xx], [map_label, iter_label, "vtd", "assignments"]
        )
        label: str = f"{map_label}_{iter_label}"

        tmpdir: str = intermediate_dir + "/" + xx
        prefix: str = map_label
        data: str = input_csv
        adjacencies: str = pairs_csv
        output: str = output_csv

        do_baseline_run(
            tmpdir, N, seed, prefix, data, adjacencies, output, label, verbose
        )

        pass


if __name__ == "__main__":
    main()

### END ###
