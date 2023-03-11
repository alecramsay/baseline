#!/usr/bin/env python3
#

"""
Make initial assignments

For example:

$ scripts/make_initial_assignments.py -s NC -v
$ scripts/make_initial_assignments.py -s GA -e -v

For documentation, type:

$ scripts/make_initial_assignments.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from typing import cast

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Equalize district populations."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-e",
        "--equalize",
        dest="equalize",
        action="store_true",
        help="Spread out overages",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Make initial assignments."""

    args: Namespace = parse_args()
    xx: str = args.state
    equalize: bool = args.equalize

    verbose: bool = args.verbose

    unit: str = "vtd"  # TODO - bg for CA & OR
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
        [xx, cycle, "block", unit], "_", "pickle"
    )
    precinct_by_block: dict[str, str] = read_pickle(rel_path)

    # Load the block population file for NC (temp/NC_2020_block_pop.pickle)

    if verbose:
        print(f"   - Loading block populations ...")

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "pop"], "_", "pickle"
    )

    pop_by_block: dict[str, int] = read_pickle(rel_path)

    # Loop over the BAF, aggregating the block populations by VTD/district combination

    if verbose:
        print(f"   - Aggregating block populations by VTD & district ...")

    total_pop: int = 0
    precinct_district_pairs: dict = defaultdict(int)
    districts_by_precinct: dict = defaultdict(set)  # Identify split precincts
    for row in block_assignments:
        block: str = row["GEOID20"]
        district: int = row["District"]
        pop: int = pop_by_block[block]
        precinct: str = precinct_by_block[block]

        assert district in range(1, n + 1)

        combo: tuple = (precinct, district)
        precinct_district_pairs[combo] += pop
        total_pop += pop

        districts_by_precinct[precinct].add(district)

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

        districts: dict[int, Any] = {
            i: {"population": 0, "blocks": [], "precincts": [], "border": []}
            for i in range(1, n + 1)
        }
        for k, v in precinct_district_pairs.items():
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
            unit_data: dict = read_pickle(graph_path)
            precinct_graph: Graph = Graph(unit_data)

            ## Invert the block & precinct assignments by district

            if verbose:
                print(f"   - Inverting block assignments by district ...")

            for row in block_assignments:
                districts[row["District"]]["blocks"].append(row["GEOID20"])

            del block_assignments

            for k, v in precinct_district_pairs.items():
                d: int = k[1]
                precinct: str = k[0]
                if len(districts_by_precinct[precinct]) == 0:
                    raise Exception(
                        f"Precinct {precinct} is not assigned to any district!"
                    )
                if len(districts_by_precinct[precinct]) > 1:
                    continue  # Ignore split precincts
                districts[d]["precincts"].append(precinct)

            # Compute a district adjacency graph

            if verbose:
                print(f"   - Computing a district adjacency graph ...")

            district_data: dict[int, list[int]] = dict()
            for k, v in districts.items():
                current: int = k
                neighbors: set[int] = set()

                for block_id in v["blocks"]:
                    precinct_id: str = precinct_by_block[block_id]
                    for neighbor in precinct_graph.neighbors(precinct_id):
                        if neighbor == OUT_OF_STATE:
                            # neighbors.add(OUT_OF_STATE)
                            continue

                        for other in districts_by_precinct[neighbor]:
                            if other != current:
                                neighbors.add(other)

                district_data[current] = list(neighbors)

            district_graph: Graph = Graph(district_data)

            # Note the border precincts for each district

            if verbose:
                print(f"   - Finding precincts on district borders ...")

            for id, data in districts.items():
                border: list[str] = border_shapes(
                    id, data["precincts"], precinct_graph, districts_by_precinct
                )
                districts[id]["border"] = border

            # Find swaps that reduce the over/under population deviations of adjacent districts

            if verbose:
                print(
                    f"   - Finding population swaps that reduce population deviations ..."
                )
                report_deviations(
                    [districts[i]["population"] for i in districts], "Before moves"
                )

            moves: list = smooth_districts(deviations, district_graph)

            # Reassign precincts to effect the moves

            for m in moves:
                from_d: int = m["from"]
                to_d: int = m["to"]
                adjustment: int = m["adjustment"]

                geiods: list[str] = on_border_with(
                    from_d,
                    to_d,
                    districts[from_d]["border"],
                    precinct_graph,
                    districts_by_precinct,
                )
                pops: list[int] = [
                    precinct_district_pairs[(id, from_d)] for id in geiods
                ]

                unsorted_precincts: dict[str, int] = dict(zip(geiods, pops))
                sorted_precincts: dict[str, int] = dict(
                    sorted(unsorted_precincts.items(), key=lambda item: item[1])
                )

                for k, v in sorted_precincts.items():
                    if v < adjustment:
                        # Move the entire precinct
                        precinct_district_pairs.pop((k, from_d), None)
                        precinct_district_pairs[(k, to_d)] += v
                        districts[from_d]["population"] -= v
                        districts[to_d]["population"] += v

                        adjustment -= v
                    else:
                        # Split the precinct
                        precinct_district_pairs[(k, from_d)] -= adjustment
                        precinct_district_pairs[(k, to_d)] += adjustment
                        districts[from_d]["population"] -= adjustment
                        districts[to_d]["population"] += adjustment
                        break  # The move is complete

            if verbose:
                report_deviations(
                    [districts[i]["population"] for i in districts], "After moves"
                )

    ### Write the results to a CSV file ###

    if verbose:
        print(f"4. Writing the results to a CSV file")

    # Load the pickled GEOID index

    if verbose:
        print(f"   - Loading the GEOID offset index ...")

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "index"], "_", "pickle"
    )
    index_by_geoid: dict = read_pickle(rel_path)

    # Write the file

    if verbose:
        print(f"   - Writing the file ...")

    splits: list[dict] = [
        {"DISTRICT": d, "VTD": index_by_geoid[v], "POP": float(p)}
        for (v, d), p in precinct_district_pairs.items()
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
