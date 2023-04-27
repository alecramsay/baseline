#!/usr/bin/env python3
#

"""
Extract a contiguity graph for a state & geographic unit.

For example:

$ scripts/extract_graph.py -s NC
$ scripts/extract_graph.py -s MI -w

$ scripts/extract_graph.py -s OR -w
$ scripts/extract_graph.py -s CA -w

For documentation, type:

$ scripts/extract_graph.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *

from libpysal.weights import Rook


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract an adjacency graph from a shapefile."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-u",
        "--unit",
        default="vtd",
        help="The geographic unit (e.g., vtd)",
        type=str,
    )
    parser.add_argument(
        "-w", "--water", dest="water", action="store_true", help="Water-only precincts"
    )

    # TODO - Connections to add

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()

    return args


def main() -> None:
    """Extract an adjacency graph from a shapefile."""

    args: Namespace = parse_args()

    xx: str = args.state
    unit: str = args.unit
    if unit != "vtd":
        raise ValueError(f"Unit {unit} not recognized.")
    if xx in ["CA", "OR"]:
        unit = "bg"
    unit_label: str = "vtd20" if unit == "vtd" else "bg"
    # "tract", "bg", "tabblock20"
    water: bool = args.water
    verbose: bool = args.verbose

    #

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    id: str = unit_id(unit)

    shp_dir: str = file_name(["tl_2020", fips, unit_label], "_")
    shp_path: str = path_to_file([rawdata_dir, xx, shp_dir]) + file_name(
        ["tl_2020", fips, unit_label], "_", "shp"
    )

    # Read the shapefile & extract the graph

    graph: Graph = Graph(shp_path, id)

    # Remove water-only precincts

    water_precincts: list = list()
    if water:
        rel_path: str = path_to_file([data_dir, xx]) + file_name(
            [xx, cycle, "water_only"], "_", "csv"
        )  # GEOID,ALAND,AWATER
        types: list = [str, int, int]
        water_precincts = [row["GEOID"] for row in read_csv(rel_path, types)]

        for w in water_precincts:
            if w in graph.nodes():
                print(f"Removing water-only precinct {w}.")
                graph.remove(w)

    # TODO - Add connections as needed

    # Make sure the graph is consistent & fully connected

    if not graph.is_consistent():
        print(f"WARNING: Graph is not consistent.")
    if not graph.is_connected():
        print(f"WARNING: Graph is not fully connected.")

    # Pickle the graph

    graph_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "graph"], "_", "pickle"
    )
    write_pickle(graph_path, graph.data())

    # Also save it as pairs in a CSV file, but ignore OUT_OF_STATE connections

    pairs_path: str = path_to_file(["data", xx]) + file_name(
        [xx, str(cycle), unit, "adjacencies"], "_", "csv"
    )
    abs_path: str = FileSpec(pairs_path).abs_path

    with open(abs_path, "w") as f:
        for one, two in graph.adjacencies():
            if one != "OUT_OF_STATE" and two != "OUT_OF_STATE":
                print(f"{one},{two}", file=f)

    pass


if __name__ == "__main__":
    main()

### END ###
