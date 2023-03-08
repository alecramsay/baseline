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

    # Get the # of districts

    n: int = districts_by_state[xx]["congress"]

    # Load the block-to-VTD (temp/NC_2020_block_vtd.pickle)

    if verbose:
        print()
        print(f"Loading {xx} block-to-VTD assignments ...")

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "vtd"], "_", "pickle"
    )
    vtd_by_block: dict = read_pickle(rel_path)

    # Load the block population file for NC (temp/NC_2020_block_pop.pickle)

    if verbose:
        print(f"Loading {xx} block populations ...")

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "pop"], "_", "pickle"
    )
    pop_by_block: dict = read_pickle(rel_path)

    # Load the pickled GEOID index (temp/NC_2020_vtd_index.pickle)

    if verbose:
        print(f"Loading {xx} GEOID index ...")

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "vtd", "index"], "_", "pickle"
    )
    index_by_geoid: dict = read_pickle(rel_path)

    # Read the BAF for the official NC map (data/NC/NC_2020_block_assignments.csv)

    if verbose:
        print(f"Loading {xx} block assignments ...")

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", "assignments"], "_", "csv"
    )
    types: list = [str, int]
    block_assignments: list = read_typed_csv(
        rel_path, types
    )  # A list of dicts like {'GEOID20': '371139703032008', 'District': 11}

    # Loop over the BAF, aggregating the block populations by VTD/district combination

    if verbose:
        print(f"Aggregating {xx} block populations by precinct ...")

    total_pop: int = 0
    vtd_district: dict = defaultdict(int)
    districts_by_vtd: dict = defaultdict(set)  # Identify split precincts
    for row in block_assignments:
        block: str = row["GEOID20"]
        district: int = row["District"]
        pop: int = pop_by_block[block]
        vtd: str = vtd_by_block[block]

        combo: tuple = (vtd, district)
        vtd_district[combo] += pop
        total_pop += pop

        districts_by_vtd[vtd].add(district)

    # Compute population by district

    if verbose:
        print(f"Computing {xx} population by district ...")

    districts: dict[int, dict] = {
        i: {"population": 0, "blocks": [], "precincts": [], "border": []}
        for i in range(1, n + 1)
    }
    for k, v in vtd_district.items():
        districts[k[1]]["population"] += v

    # TODO - Even out overages & underages

    ## Load the precinct graph

    if verbose:
        print(f"Loading {xx} precinct graph ...")

    graph_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "graph"], "_", "pickle"
    )
    data: dict = read_pickle(graph_path)
    vtd_graph: Graph = Graph(data)

    ## Invert the block & precinct assignments by district

    if verbose:
        print(f"Inverting {xx} block assignments by district ...")

    for row in block_assignments:
        districts[row["District"]]["blocks"].append(row["GEOID20"])

    del block_assignments

    for k, v in vtd_district.items():
        d: int = k[1]
        vtd: str = k[0]
        if len(districts_by_vtd[vtd]) > 1:
            continue  # Ignore split precincts
        districts[d]["precincts"].append(vtd)

    ## Compute a district adjacency graph

    if verbose:
        print(f"Computing {xx} district adjacency graph ...")

    data: dict[int, list[int]] = dict()
    for k, v in districts.items():
        current: int = k
        neighbors: set[int] = set()

        for block_id in v["blocks"]:
            vtd_id: str = vtd_by_block[block_id]
            for neighbor in vtd_graph.neighbors(vtd_id):
                if neighbor == OUT_OF_STATE:
                    # neighbors.add(OUT_OF_STATE)
                    continue

                for other in districts_by_vtd[neighbor]:
                    if other != current:
                        neighbors.add(other)

        data[current] = list(neighbors)

    district_graph: Graph = Graph(data)

    ## Note the border precincts for each district

    if verbose:
        print(f"Finding {xx} district borders ...")

    for id, data in districts.items():
        border: list[str] = border_shapes(
            id, data["precincts"], vtd_graph, vtd_district
        )
        districts[id]["border"] = border

    ## Smooth out the over/under population deviations of adjacent districts

    target_pop: int = round(total_pop / len(districts))
    deviations: dict = {k: v["population"] - target_pop for k, v in districts.items()}

    moves: dict = smooth_districts(deviations, district_graph, verbose)

    for m in moves:
        print(f"Move {m['adjustment']} from {m['from']} to {m['to']}")

    ## Reassign precincts to effect moves

    # TODO - HERE

    # Write the results to initial.csv

    # TODO

    # splits: list[dict] = [
    #     {"DISTRICT": k[1], "VTD": index_by_geoid[k[0]], "POP": float(v)}
    #     for k, v in vtd_district.items()
    # ]

    # rel_path: str = path_to_file([data_dir, xx]) + file_name(
    #     [xx, cycle, unit, "assignments"], "_", "csv"
    # )
    # write_csv(
    #     rel_path, splits, ["DISTRICT", "VTD", "POP"], precision="{:.1f}", header=False
    # )

    pass


if __name__ == "__main__":
    main()

### END ###
