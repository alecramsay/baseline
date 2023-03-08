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
    equalize: bool = True

    verbose: bool = True

    # Get the # of districts

    n: int = districts_by_state[xx]["congress"]

    ### Read the BAF for the input map ###

    if verbose:
        print()
        print(f"Making initial precint assignments for {xx}:")
        print(f"1. Loading block assignments")

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", "assignments"], "_", "csv"
    )
    types: list = [str, int]
    block_assignments: list = read_typed_csv(
        rel_path, types
    )  # A list of dicts like {'GEOID20': '371139703032008', 'District': 11}

    ### Aggregate block populations by VTD/district combination ###

    if verbose:
        print(f"2. Aggregating block populations by precinct")

    # Load the block-to-VTD mapping

    if verbose:
        print(f"   - Loading block-to-VTD assignments ...")

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "vtd"], "_", "pickle"
    )
    vtd_by_block: dict = read_pickle(rel_path)

    # Load the block population file for NC (temp/NC_2020_block_pop.pickle)

    if verbose:
        print(f"   - Loading block populations ...")

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "pop"], "_", "pickle"
    )
    pop_by_block: dict = read_pickle(rel_path)

    # Loop over the BAF, aggregating the block populations by VTD/district combination

    if verbose:
        print(f"   - Aggregating block populations by VTD & district ...")

    total_pop: int = 0
    vtd_district_pairs: dict = defaultdict(int)
    districts_by_vtd: dict = defaultdict(set)  # Identify split precincts
    for row in block_assignments:
        block: str = row["GEOID20"]
        district: int = row["District"]
        pop: int = pop_by_block[block]
        vtd: str = vtd_by_block[block]

        assert district in range(1, n + 1)

        # if vtd == "13261000015":
        #     print(f"District {district}, vtd {vtd}, block {block}, pop {pop}")

        combo: tuple = (vtd, district)
        vtd_district_pairs[combo] += pop
        total_pop += pop

        districts_by_vtd[vtd].add(district)

    ### Smooth out population deviations ###

    if verbose:
        if equalize:
            print(f"3. Smoothing out population deviations")
        else:
            print(f"3. Skipping smoothing out population deviations")

    if not equalize:
        pass

    else:
        # Compute population by district

        if verbose:
            print(f"   - Computing populations by district ...")

        districts: dict[int, dict] = {
            i: {"population": 0, "blocks": [], "precincts": [], "border": []}
            for i in range(1, n + 1)
        }
        for k, v in vtd_district_pairs.items():
            districts[k[1]]["population"] += v

        # Check if the districts are within +/-10 people of the target population

        target_pop: int = round(total_pop / len(districts))
        deviations: dict = {
            k: v["population"] - target_pop for k, v in districts.items()
        }
        districts_within_tolerance: bool = all(
            abs(v) < 10 for v in deviations.values()
        )  # +/- 10 is effectively exact

        if districts_within_tolerance:
            if verbose:
                print(
                    f"   - Districts are already within +/-10 people of the target population ..."
                )

        elif equalize:
            if verbose:
                print(f"   - Population deviations can be smoothed out ...")

            # Load the precinct graph

            if verbose:
                print(f"   - Loading the precinct graph ...")

            graph_path: str = path_to_file([temp_dir]) + file_name(
                [xx, cycle, unit, "graph"], "_", "pickle"
            )
            data: dict = read_pickle(graph_path)
            vtd_graph: Graph = Graph(data)

            ## Invert the block & precinct assignments by district

            if verbose:
                print(f"   - Inverting block assignments by district ...")

            for row in block_assignments:
                districts[row["District"]]["blocks"].append(row["GEOID20"])

            del block_assignments

            for k, v in vtd_district_pairs.items():
                d: int = k[1]
                vtd: str = k[0]
                if len(districts_by_vtd[vtd]) == 0:
                    raise Exception(f"VTD {vtd} is not assigned to any district!")
                if len(districts_by_vtd[vtd]) > 1:
                    continue  # Ignore split precincts
                districts[d]["precincts"].append(vtd)

            # Compute a district adjacency graph

            if verbose:
                print(f"   - Computing a district adjacency graph ...")

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

            # Note the border precincts for each district

            if verbose:
                print(f"   - Finding precincts on district borders ...")

            for id, data in districts.items():
                border: list[str] = border_shapes(
                    id, data["precincts"], vtd_graph, districts_by_vtd
                )
                districts[id]["border"] = border

            # Find swaps that reduce the over/under population deviations of adjacent districts

            if verbose:
                print(
                    f"   - Finding population swaps that reduce population deviations ..."
                )

            moves: dict = smooth_districts(deviations, district_graph, verbose)

            if verbose:
                for m in moves:
                    print(f"   - Move {m['adjustment']} from {m['from']} to {m['to']}")
                print()

            # Reassign precincts to effect the moves

            for m in moves:
                from_d: str = m["from"]
                to_d: str = m["to"]
                adjustment: int = m["adjustment"]
                candidates: list[str] = on_border_with(
                    from_d,
                    to_d,
                    districts[from_d]["border"],
                    vtd_graph,
                    districts_by_vtd,
                )
                print(
                    f"Find precincts to move {adjustment} from {from_d} to {to_d}: {len(candidates)} candidates"
                )

                # TODO - Pick a precinct & move it
                # TODO - Update the VTD/district pairs
                # TODO - Repeat until the adjustment is ...

                pass  # TODO

            # TODO - HERE

            pass  # TODO

    ### Write the results to a CSV file ###

    if verbose:
        print(f"4. Writing the results to a CSV file")

    # Load the pickled GEOID index

    if verbose:
        print(f"   - Loading the GEOID offset index ...")

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "vtd", "index"], "_", "pickle"
    )
    index_by_geoid: dict = read_pickle(rel_path)

    # Write the file

    if verbose:
        print(f"   - Writing the file ...")

    # splits: list[dict] = list()
    # for (v, d), p in vtd_district_pairs.items():
    #     splits.append({"DISTRICT": d, "VTD": index_by_geoid[v], "POP": float(p)})

    splits: list[dict] = [
        {"DISTRICT": d, "VTD": index_by_geoid[v], "POP": float(p)}
        for (v, d), p in vtd_district_pairs.items()
    ]

    # TODO
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
