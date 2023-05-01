#!/usr/bin/env python3
#

"""
Extract census total population from DRA block data JSON &
aggregate it by track and blockgroup (BG).

For example:

$ scripts/extract_pop.py -s NC -p -i 3
$ scripts/extract_pop.py -s NC -p -i 3 > data/NC/NC_census_log.txt

For documentation, type:

$ scripts/extract_pop.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract census population data from DRA block data JSON."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--precinct",
        dest="precinct",
        action="store_true",
        help="Generate precinct-level data",
    )
    parser.add_argument(
        "-t",
        "--tract",
        dest="tract",
        action="store_true",
        help="Generate tract-level data",
    )
    parser.add_argument(
        "-g", "--bg", dest="bg", action="store_true", help="Generate BG-level data"
    )
    parser.add_argument(
        "-i",
        "--iteration",
        default=0,
        help="The VTD census data file iteration number (e.g., 0)",
        type=int,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Extract census population data."""

    args: Namespace = parse_args()

    fips_map: dict[str, str] = STATE_FIPS

    xx: str = args.state
    fips: str = fips_map[xx]

    tracts: bool = args.tract
    bgs: bool = args.bg
    blocks: bool = True  # args.block
    vtds: bool = args.precinct
    iteration: str = "" if args.iteration == 0 else f"-{args.iteration}"

    verbose: bool = args.verbose

    state_dir: str = xx

    ### READ THE CENSUS DATA, PIVOT IT BY LEVEL, AND PICKLE IT ###

    total_pop: int = 0
    max_block_pop: int = 0
    max_tract_pop: int = 0
    ntracts: int = 0
    max_bg_pop: int = 0
    nbgs: int = 0
    max_block_pop: int = 0
    nblocks: int = 0
    max_vtd_pop: int = 0
    nvtds: int = 0

    # All this data comes from one file
    if blocks or bgs or tracts:
        rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
            [f"{cycle}vt_Census_block", fips, "data2"], "_", "json"
        )

        pop_by_block: defaultdict[str, int] = read_census_json(rel_path)
        pop_by_tract: defaultdict[str, int] = defaultdict(int)
        pop_by_bg: defaultdict[str, int] = defaultdict(int)

        for block, pop in pop_by_block.items():
            g: GeoID = GeoID(block)
            tract: str = g.tract
            bg: str = g.bg

            pop_by_tract[tract] += pop
            pop_by_bg[bg] += pop

            total_pop += pop

            if pop > max_block_pop:
                max_block_pop = pop

        if blocks:
            rel_path: str = path_to_file([temp_dir]) + file_name(
                [xx, cycle, "block", "pop"], "_", "pickle"
            )
            write_pickle(rel_path, pop_by_block)

        nblocks: int = len(pop_by_block)
        del pop_by_block

        # Tracts

        if tracts:
            for tract, pop in pop_by_tract.items():
                if pop > max_tract_pop:
                    max_tract_pop = pop

            rel_path: str = path_to_file([temp_dir]) + file_name(
                [xx, cycle, "tract", "pop"], "_", "pickle"
            )
            write_pickle(rel_path, pop_by_tract)

            ntracts: int = len(pop_by_tract)
            del pop_by_tract

        # Blockgroups

        if bgs:
            for bg, pop in pop_by_bg.items():
                if pop > max_bg_pop:
                    max_bg_pop = pop

            rel_path: str = path_to_file([temp_dir]) + file_name(
                [xx, cycle, "bg", "pop"], "_", "pickle"
            )
            write_pickle(rel_path, pop_by_bg)

            nbgs: int = len(pop_by_bg)
            del pop_by_bg

    # VTD data comes from another
    if vtds:
        rel_path: str = path_to_file([vtd_dir, state_dir]) + file_name(
            [f"{cycle}", "census", xx + iteration], "_", "csv"
        )

        unpopulated_precincts: list = list()

        # Figure out the number of columns in the file
        ncols: int = 80
        abs_path: str = FileSpec(rel_path).abs_path
        with open(abs_path, "r", encoding="utf-8-sig") as f:
            first_line: str = f.readline()
            ncols = len(first_line.split(","))

        types: list = [str] + [int] * (ncols - 1)
        census: list = read_csv(rel_path, types)

        id: str = unit_id("vtd")
        pop_by_vtd: defaultdict[str, int] = defaultdict(int)

        for row in census:
            vtd: str = row[id]
            pop: int = row["Tot_2020_tot"]

            pop_by_vtd[vtd] = pop

            if pop > max_vtd_pop:
                max_vtd_pop = pop

            if pop == 0:
                unpopulated_precincts.append({"GEOID": vtd})

            nvtds += 1

        rel_path: str = path_to_file([temp_dir]) + file_name(
            [xx, cycle, "vtd", "pop"], "_", "pickle"
        )
        write_pickle(rel_path, pop_by_vtd)

        nvtds: int = len(pop_by_vtd)
        del pop_by_vtd

        unpopulated: bool = False  # True
        if unpopulated and len(unpopulated_precincts) > 0:
            rel_path: str = path_to_file([data_dir, xx]) + file_name(
                [xx, cycle, "vtd", "unpopulated"], "_", "csv"
            )
            write_csv(rel_path, unpopulated_precincts, ["GEOID"])

    ### PRINT STATISTICS ###

    print()
    if blocks or bgs or tracts:
        print("Total population: {:,}".format(total_pop))
    if tracts:
        print(
            "Max tract population: {:,}".format(max_tract_pop),
            "# of tracts: {:,}".format(ntracts),
        )
    if bgs:
        print(
            "Max BG population: {:,}".format(max_bg_pop),
            "# of BGs: {:,}".format(nbgs),
        )
    if blocks or bgs or tracts:
        print(
            "Max block population: {:,}".format(max_block_pop),
            "# of blocks: {:,}".format(nblocks),
        )
    if vtds:
        print(
            "Max precinct (VTD) population: {:,}".format(max_vtd_pop),
            "# of blocks: {:,}".format(nvtds),
        )
    print()


if __name__ == "__main__":
    main()

### END ###
