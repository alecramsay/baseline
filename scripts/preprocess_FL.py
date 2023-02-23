#!/usr/bin/env python3
#

"""
Preprocess data for FL state.
"""

import geopandas
from geopandas import GeoDataFrame

from baseline import *


def main() -> None:
    """Preprocess modified VTD (precinct) data for FL"""

    xx: str = "FL"

    # Extract the x,y coordinates of Florida's modified VTDs
    feature_xy: dict[str, Coordinate] = dict()

    rel_path: str = path_to_file([rawdata_dir, xx]) + file_name(
        ["tabblock.vtd"], "_", "geojson"
    )
    vtds: GeoDataFrame = geopandas.read_file(rel_path)

    for idx, row in vtds.iterrows():
        geoid: str = row["id"]
        pt = row["geometry"].representative_point()
        x: float = pt.x
        y: float = pt.y
        coord: Coordinate = Coordinate(x, y)
        feature_xy[geoid] = coord
        # feature_xy[geoid] = row["geometry"].representative_point()

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "vtd", "xy"], "_", "pickle"
    )
    write_pickle(rel_path, feature_xy)

    del feature_xy

    commands: list[str] = [
        "scripts/extract_pop.py -s {xx} -p -i 3 > data/{xx}/{xx}_census_log.txt",
        # "scripts/extract_xy.py -s {xx} -p",
        "scripts/join_feature_data.py -s {xx} -p",
        "scripts/unpickle_to_csv.py -s {xx} -u vtd",
        # "scripts/unpickle_to_csv.py {xx} block",
        # "scripts/unpickle_to_csv.py {xx} bg",
    ]
    for command in commands:
        command: str = command.format(xx=xx)
        os.system(command)


if __name__ == "__main__":
    main()

### END ###
