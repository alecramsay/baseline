#!/usr/bin/env python3

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/baseline_state.py -s NC -i 1 -v -c
$ scripts/baseline_state.py -s NC -i 1 -v -d
$ scripts/baseline_state.py -s NC -i 1 -v

$ scripts/baseline_state.py -s NC > intermediate/NC/NC20C_log_100.txt

NOTE - To get STDOUT in the right order, use the -c option <<< TODO: Rationalize this
$ scripts/baseline_state.py -s NC -c > intermediate/NC/NC20C_log_100.txt

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
        default=100,
        help="The # of iterations to run (default: 100).",
        type=int,
    )

    parser.add_argument(
        "-c", "--create", dest="create_sh", action="store_true", help="Use create.sh"
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )
    parser.add_argument(
        "-d", "--debug", dest="debug", action="store_true", help="Debug mode"
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

    create_sh: bool = args.create_sh
    verbose: bool = args.verbose
    debug: bool = args.debug

    unit: str = "vtd"
    unit_label: str = "vtd20"

    if xx in ["CA"]:
        unit = "bg"
        unit_label = "bg"
        # unit = "tract"
        # unit_label = "tract"
    elif xx in ["OR"]:
        unit = "bg"
        unit_label = "bg"

    assert create_sh

    # DEBUG

    # Add dccvt to the path

    path_list: list[str] = [
        "/Users/alecramsay/iCloud/dev/dccvt/examples/redistricting",
        "/Users/alecramsay/iCloud/dev/dccvt/bin",
    ]
    os.environ["PATH"] += os.pathsep + os.pathsep.join(path_list)

    # Set up

    print()
    print(f">>> GENERATING BASELINE CANDIDATES FOR {xx} <<<")

    map_label: str = label_map(xx, plan_type)  # e.g., "NC20C"
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]

    data_csv: str = full_path([data_dir, xx], [xx, cycle, unit, "data"])
    adjacencies_csv: str = full_path([data_dir, xx], [xx, cycle, unit, "adjacencies"])
    tmpdir: str = intermediate_dir + "/" + xx

    start: int = K * N * int(fips)

    # Iterate creating baseline maps

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)
        output_csv: str = full_path(
            [intermediate_dir, xx], [map_label, iter_label, "vtd", "assignments"]
        )
        label: str = f"{map_label}_{iter_label}"

        if create_sh:
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
        # NOTE - Commented out alternative to using create.sh.
        # else:
        #     create_baseline_candidate(
        #         tmpdir=tmpdir,
        #         N=N,
        #         seed=seed,
        #         prefix=map_label,
        #         data=data_csv,
        #         adjacencies=adjacencies_csv,
        #         label=label,
        #         output=output_csv,
        #         verbose=verbose,
        #         debug=debug,
        #     )

        pass  # for a breakpoint

    print()


if __name__ == "__main__":
    main()

### END ###
