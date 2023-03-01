#!/usr/bin/env python3
#

"""
TODO
Extract contiguity graphs for a state's tracts, blockgroups, and blocks.

For example:

$ scripts/extract_graph.py MD
$ scripts/extract_graph.py NC
$ scripts/extract_graph.py PA
$ scripts/extract_graph.py VA
$ scripts/extract_graph.py NY

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
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()

    return args


def graph_shapes(rel_path: str, id_field: str) -> Rook:
    abs_path: str = FileSpec(rel_path).abs_path

    g: Rook = Rook.from_shapefile(abs_path, id_field)
    g = g.neighbors  # Get rid of all the extraneous PySAL stuff

    check_graph(g)

    return g


def check_graph(graph) -> bool:
    """
    Make sure each node is in every neighbor's neighbor list
    """
    consistent: bool = True

    for from_geo, neighbor_geos in graph.items():
        for to_geo in neighbor_geos:
            neighbors_neighbors = graph[to_geo]
            if from_geo in neighbors_neighbors:
                pass
            else:
                consistent = False

    if not consistent:
        print("> WARNING: This graph is not internally consistent! <")

    return consistent


def main() -> None:
    """Extract an adjacency graph from a shapefile."""

    args: Namespace = parse_args()

    fips_map: dict[str, str] = make_state_codes()

    xx: str = args.state
    fips: str = fips_map[xx]
    unit: str = args.unit
    if unit == "vtd":
        if xx in ["CA", "OR"]:
            unit = "bg"
        unit_label: str = "vtd20" if unit == "vtd" else "bg"
    else:
        raise ValueError(f"Unit {unit} not recognized.")

    verbose: bool = args.verbose

    ### CONSTRUCT PATHS ###

    state_dir: str = xx

    # tract_dir: str = file_name(["tl_2020", fips, "tract"], "_")
    # bg_dir: str = file_name(["tl_2020", fips, "bg"], "_")
    # block_dir: str = file_name(["tl_2020", fips, "tabblock20"], "_")
    precinct_dir: str = file_name(["tl_2020", fips, unit_label], "_")

    id: str = unit_id(unit)
    shp_path: str = path_to_file([rawdata_dir, state_dir, precinct_dir]) + file_name(
        ["tl_2020", fips, unit_label], "_", "shp"
    )

    # units: list[str] = ["tract", "bg", "block", unit]
    # shp_paths: list[str] = [
    #     path_to_file([rawdata_dir, state_dir, tract_dir])
    #     + file_name(["tl_2020", fips, "tract"], "_", "shp"),
    #     path_to_file([rawdata_dir, state_dir, bg_dir])
    #     + file_name(["tl_2020", fips, "bg"], "_", "shp"),
    #     path_to_file([rawdata_dir, state_dir, block_dir])
    #     + file_name(["tl_2020", fips, "tabblock20"], "_", "shp"),
    #     path_to_file([rawdata_dir, state_dir, precinct_dir])
    #     + file_name(["tl_2020", fips, unit_label], "_", "shp"),
    # ]

    # ids: list[str] = [unit_id(x) for x in units]
    # ids: list[str] = ["GEOID", "GEOID", "GEOID20"]

    # graph_paths: list[str] = [
    #     path_to_file([data_dir, state_dir])
    #     + file_name([xx, cycle, "tract", "graph"], "_", "pickle"),
    #     path_to_file([data_dir, state_dir])
    #     + file_name([xx, cycle, "bg", "graph"], "_", "pickle"),
    #     path_to_file([data_dir, state_dir])
    #     + file_name([xx, cycle, "block", "graph"], "_", "pickle"),
    # ]

    ### TODO - READ THE SHAPEFILES, EXTRACT THE GRAPHS, AND PICKLE THEM ###

    # for unit, shp_path, id, graph_path in zip(units, shp_paths, ids, graph_paths):
    print("Extracting", unit, "graph for {xx} ...")

    graph: Rook = graph_shapes(shp_path, id)
    # write_pickle(graph_path, graph)
    pass  # TODO


if __name__ == "__main__":
    main()

### END ###
