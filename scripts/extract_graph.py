#!/usr/bin/env python3
#

"""
Extract a contiguity graphs for a state's tracts, blockgroups, and blocks.

For example:

$ scripts/extract_graph.py -s NC
$ scripts/extract_graph.py -s MI -w

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

    fips_map: dict[str, str] = make_state_codes()

    xx: str = args.state

    fips: str = fips_map[xx]

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
        water_precincts = [row["GEOID"] for row in read_typed_csv(rel_path, types)]

        for w in water_precincts:
            if w in graph.nodes():
                print(f"Removing water-only precinct {w}.")
                graph.remove(w)

    # TODO - Add connections as needed

    # Make sure the graph is consistent & fully connected

    if not graph.is_consistent():
        raise ValueError("Graph is not consistent.")
    if not graph.is_connected():
        raise ValueError("Graph is not fully connected.")

    # Pickle the graph

    graph_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "graph"], "_", "pickle"
    )
    write_pickle(graph_path, graph.data())

    # Also save it as pairs in a CSV file, but ignore OUT_OF_STATE connections

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "index"], "_", "pickle"
    )
    index_by_geoid: dict = read_pickle(rel_path)

    pairs_path: str = path_to_file(["data", xx]) + file_name(
        [xx, str(cycle), unit, "pairs"], "_", "csv"
    )
    abs_path: str = FileSpec(pairs_path).abs_path

    with open(abs_path, "w") as f:
        for geoid, neighbor_geoids in graph.data().items():
            if geoid == OUT_OF_STATE:
                continue
            for neighbor in neighbor_geoids:
                if neighbor == OUT_OF_STATE:
                    continue
                x: int = index_by_geoid[geoid]
                y: int = index_by_geoid[neighbor]
                print(Pair(x, y), file=f)

    pass


if __name__ == "__main__":
    main()

### END ###
