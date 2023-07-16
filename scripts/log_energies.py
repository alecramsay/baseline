#!/usr/bin/env python3

"""
Log energies for all the maps generated for a state

For example:

$ scripts/log_energies.py -s AZ -v > intermediate/AZ/AZ20C_log_energies.txt
$ scripts/log_energies.py -s CA -v > intermediate/Ca/CA20C_log_energies.txt

For documentation, type:

$ scripts/log_energies.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def calc_energy(
    *, assignments_csv: str, data_csv: str, label: str, debug: bool = False
) -> None:
    """Compute the energy for a map.

    python3 ../dccvt/examples/redistricting/geoid.py energy \
    --assignment  /Users/alecramsay/iCloud/dev/baseline/intermediate/AZ/AZ20C_I000K01N09_vtd_assignments.csv \
    --redistricting_input /Users/alecramsay/iCloud/dev/baseline/data/AZ/AZ_2020_vtd_data.csv \
	--label AZ20C_I000K01N09
    """

    command: str = f"python3  {dccvt_py}/geoid.py energy --assignment  {assignments_csv} --redistricting_input {data_csv} --label {label}"
    os.system(command)


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Find districts that minimize population compactness."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="AZ",
        help="The two-character state code (e.g., AZ)",
        type=str,
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Log energies for all the maps generated for a state."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = "congress"
    unit: str = "vtd"
    if xx == "CA":
        unit = "bg"
        # unit = "tract"
    elif xx in ["OR", "WV", "HI"]:
        unit = "bg"
    iterations: int = 100

    verbose: bool = args.verbose

    # Constants

    map_label: str = label_map(xx, plan_type)
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]
    start: int = K * N * int(fips)

    # Get the list of candidate maps

    candidates_path: str = path_to_file([maps_dir, xx]) + file_name(
        [map_label, "candidates"], "_", "csv"
    )
    candidates_data: list[dict] = read_csv(
        candidates_path, [int, str, str, float, float, float, float, float, float]
    )
    candidates: list[str] = [row["MAP"] for row in candidates_data]

    # Log the (correct) energies for each map

    for map_name in candidates:
        assignments_csv: str = full_path(
            [intermediate_dir, xx], [map_name, "vtd", "assignments"]
        )
        data_csv: str = full_path([data_dir, xx], [xx, cycle, unit, "data"])
        calc_energy(
            assignments_csv=assignments_csv,
            data_csv=data_csv,
            label=map_name,
            debug=verbose,
        )
        # Energy for map AZ20C_I000K01N09 = 3099496.0532179917

    pass


if __name__ == "__main__":
    main()

### END ###
