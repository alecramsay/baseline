#!/usr/bin/env python3

"""
Pull energies for all iterations from a log file.

For example:

$ scripts/pull_energies.py -s NC -i 10 -v
$ scripts/pull_energies.py -s NC -i 100 -v
$ scripts/pull_energies.py -s NC -i 1000 -v

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


def main() -> None:
    """Extract map energies from a log file."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = args.map
    iterations: int = args.iterations

    verbose: bool = args.verbose

    #

    fips: str = STATE_FIPS[xx]
    map_label: str = label_map(xx, plan_type)

    log_txt: str = full_path(
        [intermediate_dir, xx], [map_label, "log", str(iterations)], "txt"
    )
    energies_csv: str = full_path(
        [intermediate_dir, xx], [map_label, "energies", str(iterations)]
    )

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

    result: str
    parts: list[str]
    name: str = "N/A"
    regions: int
    energy: float
    contiguous: bool = False

    for line in lines:
        if line.startswith("Map "):
            # Map NC20C_I000K01N14 = Contiguous 14
            # Map NC20C_I018K01N14 = Discontiguous 15 != 14
            result = line[4:].strip()
            parts = [x.strip() for x in result.split("=")]

            name = label_iteration(i, K, N)  # parts[0]
            contiguous = True if parts[1].split(" ")[0] == "Contiguous" else False

            continue

        if line.startswith("Energy for map "):
            # Energy for map NC20C_I000K01N14 = 3100302.685077957

            result = line[15:].strip()
            parts = [x.strip() for x in result.split("=")]

            again: str = label_iteration(i, K, N)  # parts[0]
            if again != name:
                raise ValueError(f"Unexpected map name: {name} != {again}")

            energy = float(parts[1])

            if energy < lowest:
                lowest = energy
                lowest_map = name

            maps.append({"MAP": name, "ENERGY": energy, "CONTIGUOUS": contiguous})

            i += 1
            continue

    print(f"Lowest energy map: {lowest_map}")

    for m in maps:
        name = m["MAP"]
        energy = m["ENERGY"]
        delta: float = (energy - lowest) / lowest
        note: str = "" if name != lowest_map else "<---"

        m["DELTA"] = delta
        m["NOTE"] = note

    write_csv(
        energies_csv,
        maps,
        ["MAP", "ENERGY", "DELTA", "CONTIGUOUS", "NOTE"],
        precision="{:.6f}",
    )


pass


if __name__ == "__main__":
    main()

### END ###
