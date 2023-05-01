#!/usr/bin/env python3
#

"""
Extract data for FL.

For example:

$ scripts/extract_FL.py

"""

import geopandas
from geopandas import GeoDataFrame

from baseline import *


def main() -> None:
    """Preprocess modified VTD (precinct) data for FL"""

    xx: str = "FL"
    # water: bool = True
    adds: bool = False
    unpopulated: bool = False  # True

    ### Read DRA's GeoJSON file of corrects Florida VTDs ###

    print("Reading the GeoJSON file ...")

    feature_xy: dict[str, Coordinate] = dict()

    rel_path: str = path_to_file([rawdata_dir, xx]) + file_name(
        ["tabblock.vtd"], "_", "geojson"
    )
    vtds: GeoDataFrame = geopandas.read_file(rel_path)

    ### Extract x,y coordinates for each VTD & pickle the results ###

    print("Extracting the x,y coordinates ...")

    for idx, row in vtds.iterrows():
        geoid: str = row["id"]
        pt = row["geometry"].representative_point()
        x: float = pt.x
        y: float = pt.y
        coord: Coordinate = Coordinate(x, y)
        feature_xy[geoid] = coord

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "vtd", "xy"], "_", "pickle"
    )
    write_pickle(rel_path, feature_xy)

    del feature_xy

    ### Do the normal extract_data subcommands, except skip extracting x,y coordinates done above ###

    print("Extracting the other data ...")

    commands: list[str] = [
        "scripts/extract_pop.py -s {xx} -p -i 3 > data/{xx}/{xx}_census_log.txt",
        # "scripts/extract_xy.py -s {xx} -p", # NOTE - Points extracted from DRA shapes above
        "scripts/join_feature_data.py -s {xx} -p",
        "scripts/unpickle_to_csv.py -s {xx} -u vtd",  # NOTE - Not removing water-only precincts
        "scripts/unpickle_to_csv.py -s {xx} -u block",
        "scripts/extract_block_vtds.py -s {xx}",
        "scripts/extract_name_map.py -s {xx} > data/{xx}/{xx}_2020_vtd_names.txt",
    ]
    for command in commands:
        command: str = command.format(xx=xx)
        os.system(command)

    ### Extract the graph here -- in lieu of `scripts/extract_graph.py -s FL -w` ###

    print("Extracting the graph ...")

    unit: str = "vtd"
    id: str = "id"  # unit_id(unit)
    graph: Graph = Graph(vtds, id)

    # Add connections as needed to make the graph derived from shapes fully connected

    if adds:
        adds_path: str = path_to_file([data_dir, xx]) + file_name(
            [xx, cycle, unit, "contiguity_mods"], "_", "csv"
        )
        mods: list = read_mods(adds_path)
        # NOTE - Assume all mods are additions. Nothing else is supported yet.

        for mod in mods:
            graph.add_adjacency(mod[1], mod[2])

    # NOTE - Again, not removing water-only precincts here, because the corrected
    # shapes from DRA don't contain the necessary information.

    # Remove water-only precincts

    # print("Removing water-only precincts ...")

    # water_precincts: list = list()
    # if water:
    #     water_path: str = path_to_file([data_dir, xx]) + file_name(
    #         [xx, cycle, unit, "water_only"], "_", "csv"
    #     )  # GEOID,ALAND,AWATER
    #     types: list = [str, int, int]
    #     water_precincts = [row["GEOID"] for row in read_csv(water_path, types)]

    #     for w in water_precincts:
    #         if w in graph.nodes():
    #             print(f"Removing water-only precinct {w}.")
    #             graph.remove(w)

    # Bridge over unpopulated precincts

    if unpopulated:
        unpopulated_path: str = path_to_file([data_dir, xx]) + file_name(
            [xx, cycle, "vtd", "unpopulated"], "_", "csv"
        )  # NOTE - Only works for vtds right now
        types: list = [str]
        unpopulated_precincts = [
            row["GEOID"] for row in read_csv(unpopulated_path, types)
        ]

        print("Bridging over unpopulated precincts.")
        for z in unpopulated_precincts:
            if z in graph.nodes():
                graph.bridge(z)

    # Make sure the graph is consistent & fully connected

    print("Checking the graph ...")

    if not graph.is_consistent():
        print(f"WARNING: Graph is not consistent.")
    if not graph.is_connected():
        print(f"WARNING: Graph is not fully connected.")

    # Pickle the graph

    print("Pickling the graph & saving adjacencies ...")

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

    pass  # for a debugging breakpoint


if __name__ == "__main__":
    main()

### END ###
