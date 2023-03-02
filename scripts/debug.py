#!/usr/bin/env python3

"""
DEBUG
"""

from baseline import *

xx: str = "NC"
unit: str = "vtd"
unit_label: str = "vtd20"

fips_map: dict[str, str] = make_state_codes()
fips: str = fips_map[xx]
id: str = unit_id(unit)

#

shp_dir: str = file_name(["tl_2020", fips, unit_label], "_")
shp_path: str = path_to_file([rawdata_dir, xx, shp_dir]) + file_name(
    ["tl_2020", fips, unit_label], "_", "shp"
)

unit_graph: Graph = Graph(shp_path, id)

print(f"Out of state: {len(unit_graph.neighbors(OUT_OF_STATE))}")

pass

"""
g: dict = {
    1: [2, 3, 4, 13],
    2: [9, 4, 13, 1],
    3: [1, 13, 7],
    4: [9, 2, 6, 1],
    5: [8, 10, 11, 6],
    6: [8, 9, 4, 5],
    7: [9, 3, 13],
    8: [5, 6, 9, 10, 12, 14],
    9: [2, 4, 6, 7, 8, 13],
    10: [5, 8, 11, 12, 14],
    11: [10, 5],
    12: [8, 10, 14],
    13: [1, 2, 3, 7, 9],
    14: [8, 10, 12],
}
"""

### END ###
