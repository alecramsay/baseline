#!/usr/bin/env python3

"""
DEBUG
"""

from baseline import *


xx: str = "UT"
unit: str = "vtd"
id: str = unit_id(unit)

#

unit_label: str = "vtd20" if unit == "vtd" else unit

fips_map: dict[str, str] = STATE_FIPS
fips: str = fips_map[xx]

#

shp_dir: str = file_name(["tl_2020", fips, unit_label], "_")
shp_path: str = path_to_file([rawdata_dir, xx, shp_dir]) + file_name(
    ["tl_2020", fips, unit_label], "_", "shp"
)

#

graph: Graph = Graph(shp_path, id)

pass

### END ###
