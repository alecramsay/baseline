#!/usr/bin/env python3

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/rebaseline_NC.py > rebaseline/NC20C_log_100.txt

For documentation, type:

$ scripts/rebaseline_NC.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


@time_function
def main() -> None:
    """Find districts that minimize population compactness."""

    args: Namespace = parse_args()

    xx: str = "NC"  # args.state
    plan_type: str = args.map
    iterations: int = args.iterations

    verbose: bool = args.verbose
    debug: bool = args.debug

    unit: str = study_unit(xx)

    # DEBUG

    # END DEBUG

    # Add dccvt to the path

    path_list: list[str] = [
        "/Users/alecramsay/iCloud/dev/dccvt/examples/redistricting",
        "/Users/alecramsay/iCloud/dev/dccvt/bin",
    ]
    os.environ["PATH"] += os.pathsep + os.pathsep.join(path_list)

    rebaseline_dir: str = "rebaseline"

    # Set up

    print()
    print(f">>> RE-GENERATING BASELINE CANDIDATES FOR {xx} <<<")

    map_label: str = label_map(xx, plan_type)  # e.g., "NC20C"
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]

    data_csv: str = full_path([data_dir, xx], [xx, cycle, unit, "data"])
    adjacencies_csv: str = full_path([data_dir, xx], [xx, cycle, unit, "adjacencies"])
    tmpdir: str = rebaseline_dir

    start: int = K * N * int(fips)

    # Iterate creating baseline maps

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)
        output_csv: str = full_path(
            [rebaseline_dir], [map_label, iter_label, "vtd", "assignments"]
        )
        label: str = f"{map_label}_{iter_label}"

        execute_create_sh(
            tmpdir=tmpdir,
            N=N,
            seed=seed,
            prefix=map_label,
            data=data_csv,
            adjacencies=adjacencies_csv,
            label=label,
            output=output_csv,
            verbose=verbose,
        )

    print()


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Find districts that minimize population compactness."
    )

    # parser.add_argument(
    #     "-s",
    #     "--state",
    #     default="NC",
    #     help="The two-character state code (e.g., NC)",
    #     type=str,
    # )
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

    # parser.add_argument(
    #     "-c", "--create", dest="create_sh", action="store_true", help="Use create.sh"
    # )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )
    parser.add_argument(
        "-d", "--debug", dest="debug", action="store_true", help="Debug mode"
    )

    args: Namespace = parser.parse_args()
    return args


if __name__ == "__main__":
    main()

### END ###
