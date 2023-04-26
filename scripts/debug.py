#!/usr/bin/env python3

"""
DEBUG
"""

from baseline import *


xx: str = "KS"
unit: str = "vtd"
unit_label: str = "vtd20"
water: bool = True
verbose: bool = True


def main() -> None:
    # Unpickle the graph

    graph_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "graph"], "_", "pickle"
    )
    data: dict = read_pickle(graph_path)

    g: Graph = Graph(data)

    # Remove water-only precincts

    water_precincts: list = list()
    if water:
        rel_path: str = path_to_file([data_dir, xx]) + file_name(
            [xx, cycle, "water_only"], "_", "csv"
        )  # GEOID,ALAND,AWATER
        types: list = [str, int, int]
        water_precincts = [row["GEOID"] for row in read_csv(rel_path, types)]

        for w in water_precincts:
            if w in g.nodes():
                print(f"Removing water-only precinct {w}.")
                g.remove(w)

    print(f"Graph is consistent: {g.is_consistent()}")
    print(f"Graph is connected: {g.is_connected()}")

    pass


if __name__ == "__main__":
    main()

### END ###
