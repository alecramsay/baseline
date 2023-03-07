#!/usr/bin/env python3

"""
DEBUG
"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict

from baseline import *


def main() -> None:
    """DEBUG"""

    # Hard code args for testing

    xx: str = "GA"
    unit: str = "vtd"

    verbose: bool = True

    # Load the block-to-VTD (temp/NC_2020_block_vtd.pickle)

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "vtd"], "_", "pickle"
    )
    vtd_by_block: dict = read_pickle(rel_path)

    # Load the block population file for NC (temp/NC_2020_block_pop.pickle)

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "pop"], "_", "pickle"
    )
    pop_by_block: dict = read_pickle(rel_path)

    # Load the pickled GEOID index (temp/NC_2020_vtd_index.pickle)

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "vtd", "index"], "_", "pickle"
    )
    index_by_geoid: dict = read_pickle(rel_path)

    # Read the BAF for the official NC map (data/NC/NC_2020_block_assignments.csv)

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", "assignments"], "_", "csv"
    )
    types: list = [str, int]
    block_assignments: list = read_typed_csv(
        rel_path, types
    )  # A list of dicts like {'GEOID20': '371139703032008', 'District': 11}

    # Loop over the BAF, aggregating the block populations by VTD/district combination

    vtd_district: dict = defaultdict(int)
    for row in block_assignments:
        block: str = row["GEOID20"]
        district: int = row["District"]
        pop: int = pop_by_block[block]
        vtd: str = vtd_by_block[block]

        combo: tuple = (vtd, district)
        vtd_district[combo] += pop

    # Report population by district

    if verbose:
        district_pop: dict = defaultdict(int)
        for k, v in vtd_district.items():
            district_pop[k[1]] += v

        print()
        print(f"Population by district for {xx}")
        for k, v in sorted(district_pop.items()):
            print(f"{k:2d}: {v:8.0f}")
        print()

    # Write the results to initial.csv

    splits: list[dict] = [
        {"DISTRICT": k[1], "VTD": index_by_geoid[k[0]], "POP": float(v)}
        for k, v in vtd_district.items()
    ]

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "assignments"], "_", "csv"
    )
    write_csv(
        rel_path, splits, ["DISTRICT", "VTD", "POP"], precision="{:.1f}", header=False
    )

    pass


if __name__ == "__main__":
    main()

### END ###
