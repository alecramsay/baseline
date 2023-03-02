#!/usr/bin/env python3
#

"""
Extract a contiguity graphs for a state's tracts, blockgroups, and blocks.

For example:

$ scripts/extract_graph.py -s NC -u vtd

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

    # if not consistent:
    #     print("> WARNING: This graph is not internally consistent! <")

    return consistent


class Pair(NamedTuple):
    one: int
    two: int

    def __repr__(self) -> str:
        return f"{self.one},{self.two}"


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

    verbose: bool = args.verbose

    #

    id: str = unit_id(unit)
    shp_dir: str = file_name(["tl_2020", fips, unit_label], "_")
    shp_path: str = path_to_file([rawdata_dir, xx, shp_dir]) + file_name(
        ["tl_2020", fips, unit_label], "_", "shp"
    )

    # Read the shapefile & extract the graph

    graph: Rook = graph_shapes(shp_path, id)

    consistent: bool = check_graph(graph)
    if not consistent:
        raise ValueError("Graph is not internally consistent!")

    # TODO - Remove water-only precincts <<< N/A for NC

    # TODO - Add connections <<< N/A for NC

    # TODO - Make sure the graph is fully connected
    connected: bool = True

    # TODO - If not, find & report "islands"

    # Save the neighbors

    rel_path: str = path_to_file(["data", xx]) + file_name(
        [xx, str(cycle), unit, "pairs"], "_", "csv"
    )
    abs_path: str = FileSpec(rel_path).abs_path

    with open(abs_path, "w") as f:
        for geoid, neighbor_geoids in graph.items():
            for neighbor in neighbor_geoids:
                print(Pair(geoid, neighbor), file=f)

    pass  # TODO


if __name__ == "__main__":
    main()

### END ###