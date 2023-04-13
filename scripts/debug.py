#!/usr/bin/env python3

"""
DEBUG
"""

from baseline import *


@time_function
def main() -> None:
    """Find districts that minimize population compactness."""

    ## Hardcode the arguments for debugging.

    xx: str = "AZ"
    plan_type: str = "congress"
    iterations: int = 100

    verbose: bool = True

    ## From here down is a clone of baseline_state.py for debugging.

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

    input_csv: str = full_path([data_dir, xx], [xx, cycle, "vtd", "data"])
    pairs_csv = full_path([data_dir, xx], [xx, cycle, "vtd", "pairs"])

    start: int = K * N * int(fips)

    # Iterate creating baseline maps

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)
        output_csv: str = full_path(
            [intermediate_dir, xx], [map_label, iter_label, "vtd", "assignments"]
        )
        label: str = f"{map_label}_{iter_label}"

        tmpdir: str = intermediate_dir + "/" + xx
        prefix: str = map_label
        data: str = input_csv
        adjacencies: str = pairs_csv
        output: str = output_csv

        print(f"Iteration {i + 1} of {iterations} (seed {seed})")

        execute_create_sh(
            tmpdir, N, seed, prefix, data, adjacencies, output, label, verbose
        )

        pass


if __name__ == "__main__":
    main()

### END ###
