#!/usr/bin/env python3

"""
Cull energies for all the maps into a CSV

For example:

$ scripts/energies_to_csv.py -s AZ -v 

For documentation, type:

$ scripts/energies_to_csv.py -h
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
    """Cull energies for a state's maps into a CSV."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = "congress"
    unit: str = "vtd"
    iterations: int = 100

    verbose: bool = args.verbose

    # Constants

    map_label: str = label_map(xx, plan_type)
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier
    fips: str = STATE_FIPS[xx]
    start: int = K * N * int(fips)

    # Pull the energies from the log file

    log_txt: str = full_path(
        [intermediate_dir, xx], [map_label, "log", "energies"], "txt"
    )
    abs_path: str = FileSpec(log_txt).abs_path
    with open(abs_path, "r") as f:
        lines: list[str] = list()
        line: str = f.readline()
        while line:
            lines.append(line)

            line = f.readline()

    # Parse the energies

    candidates: list[dict] = list()
    for line in lines:
        if line.startswith("Energy for map "):
            # Energy for map NC20C_I000K01N14 = 3100302.685077957

            result = line[15:].strip()
            parts = [x.strip() for x in result.split("=")]

            name = parts[0]
            energy = float(parts[1])

            candidates.append(
                {
                    "MAP": name,
                    "ENERGY": energy,
                }
            )

            continue

    # Sort the maps by name

    candidates = sorted(candidates, key=lambda plan: plan["MAP"])

    # Write energies to a CSV file

    energies_csv: str = path_to_file([maps_dir, xx]) + file_name(
        [map_label, "energies"], "_", "csv"
    )

    write_csv(
        energies_csv,
        candidates,
        [
            "MAP",
            "ENERGY",
        ],
        precision="{:.6f}",
    )

    pass


if __name__ == "__main__":
    main()

### END ###
