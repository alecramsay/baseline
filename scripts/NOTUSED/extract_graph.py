#!/usr/bin/env python3
#

"""
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


### PARSE ARGS ###

parser: ArgumentParser = argparse.ArgumentParser(
    description="Find population compact districts."
)

parser.add_argument("state", help="The two-character state code (e.g., MD)", type=str)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()
fips_map: dict[str, str] = STATE_FIPS

xx: str = args.state
fips: str = fips_map[xx]
verbose: bool = args.verbose


### CONSTRUCT PATHS ###

state_dir: str = xx

tract_dir: str = file_name(["tl_2020", fips, "tract"], "_")
bg_dir: str = file_name(["tl_2020", fips, "bg"], "_")
block_dir: str = file_name(["tl_2020", fips, "tabblock20"], "_")

units: list[str] = ["tract", "bg", "block"]
shp_paths: list[str] = [
    path_to_file([rawdata_dir, state_dir, tract_dir])
    + file_name(["tl_2020", fips, "tract"], "_", "shp"),
    path_to_file([rawdata_dir, state_dir, bg_dir])
    + file_name(["tl_2020", fips, "bg"], "_", "shp"),
    path_to_file([rawdata_dir, state_dir, block_dir])
    + file_name(["tl_2020", fips, "tabblock20"], "_", "shp"),
]

ids: list[str] = ["GEOID", "GEOID", "GEOID20"]

graph_paths: list[str] = [
    path_to_file([data_dir, state_dir])
    + file_name([xx, cycle, "tract", "graph"], "_", "pickle"),
    path_to_file([data_dir, state_dir])
    + file_name([xx, cycle, "bg", "graph"], "_", "pickle"),
    path_to_file([data_dir, state_dir])
    + file_name([xx, cycle, "block", "graph"], "_", "pickle"),
]


### HELPERS ###


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


### READ THE SHAPEFILES, EXTRACT THE GRAPHS, AND PICKLE THEM ###

x: str = shp_paths[0]

for unit, shp_path, id, graph_path in zip(units, shp_paths, ids, graph_paths):
    print("Extracting", unit, "graph ...")
    graph: Rook = graph_shapes(shp_path, id)
    write_pickle(graph_path, graph)

pass
