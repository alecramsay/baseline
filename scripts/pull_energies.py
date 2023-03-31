#!/usr/bin/env python3

"""
Pull energies for all iterations from a log file.

For example:

$ scripts/pull_energies.py -s NC -v > intermediate/NC/NC_2020_congress_log.txt

For documentation, type:

$ scripts/pull_energies.py -h
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
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Extract map energies from a log file."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = args.map

    verbose: bool = args.verbose

    #

    map_label: str = label_map(xx, plan_type)
    log_txt: str = full_path([intermediate_dir, xx], [map_label, "log"], "txt")
    energies_csv: str = full_path([intermediate_dir, xx], [map_label, "energies"])

    #

    abs_path: str = FileSpec(log_txt).abs_path
    with open(abs_path, "r") as f:
        lines: list[str] = list()
        line: str = f.readline()
        while line:
            lines.append(line)

            line = f.readline()

    maps: list[dict] = list()
    lowest: float = 1e9
    lowest_map: str = ""
    i: int = 0
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier

    for line in lines:
        if line.startswith("Energy for map "):
            result = line[15:].strip()
            parts: list[str] = [x.strip() for x in result.split("=")]

            name: str = label_iteration(i, K, N)  # parts[0]
            energy: float = float(parts[1])

            if energy < lowest:
                lowest = energy
                lowest_map = name

            maps.append({"MAP": name, "ENERGY": energy})
            i += 1

    print(f"Lowest energy map: {lowest_map}")

    for m in maps:
        name: str = m["MAP"]
        energy: float = m["ENERGY"]
        delta: float = (energy - lowest) / lowest
        note: str = "" if name != lowest_map else "<---"

        m["DELTA"] = delta
        m["NOTE"] = note

    write_csv(
        energies_csv, maps, ["MAP", "ENERGY", "DELTA", "NOTE"], precision="{:.6f}"
    )


pass


if __name__ == "__main__":
    main()

### END ###
