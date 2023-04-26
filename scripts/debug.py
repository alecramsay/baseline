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
    graph_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "graph"], "_", "pickle"
    )
    data: dict = read_pickle(graph_path)

    g: Graph = Graph(data)

    print(f"Graph is consistent: {g.is_consistent()}")
    print(f"Graph is connected: {g.is_connected()}")

    pass


if __name__ == "__main__":
    main()

### END ###
