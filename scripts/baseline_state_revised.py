#!/usr/bin/env python3

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/baseline_state_revised.py -s NC -i 100 -v > intermediate/NC/NC20C_log_100.txt

For documentation, type:

$ scripts/baseline_state_revised.py -h

TODO - Rename this script.
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
        default=100,
        help="The # of iterations to run (default: 100).",
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
    verbose = True  # TODO - Remove this line.

    # Add dccvt to the path

    path_list: list[str] = [
        "/Users/alecramsay/iCloud/dev/dccvt/examples/redistricting",
        "/Users/alecramsay/iCloud/dev/dccvt/bin",
    ]
    os.environ["PATH"] += os.pathsep + os.pathsep.join(path_list)

    # Set up

    map_label: str = label_map(xx, plan_type)  # e.g., "NC20C"
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]

    data_csv: str = full_path([data_dir, xx], [xx, cycle, "vtd", "data"])
    pairs_csv = full_path([data_dir, xx], [xx, cycle, "vtd", "pairs"])

    start: int = K * N * int(fips)

    # Iterate creating baseline map candidates

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)
        output_csv: str = full_path(
            [intermediate_dir, xx], [map_label, iter_label, "vtd", "assignments"]
        )
        label: str = f"{map_label}_{iter_label}"

        create_baseline_candidate(
            tmpdir=intermediate_dir + "/" + xx,
            N=N,
            seed=seed,
            prefix=map_label,
            data=data_csv,
            adjacencies=pairs_csv,
            label=label,
            output=output_csv,
            verbose=verbose,
        )


if __name__ == "__main__":
    main()

### END ###
