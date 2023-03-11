#!/usr/bin/env python3
#

"""
Preprocess data for CA.

For example:

$ scripts/preprocess_CA.py 
"""

import geopandas
from geopandas import GeoDataFrame

from baseline import *


def main() -> None:
    """Preprocess the tracts & block groups for CA."""

    commands: list[str] = [
        "scripts/extract_pop.py -s CA -t -g -i 3 > data/CA/CA_census_log.txt",
        "scripts/extract_xy.py -s CA -t -g",
        "scripts/join_feature_data.py -s CA -t -g",
        "scripts/unpickle_to_csv.py -s CA -u tract",
        "scripts/unpickle_to_csv.py -s CA -u bg",
        "scripts/index_geoids.py -s CA",
        "scripts/extract_block_bgs.py -s CA",
    ]
    for command in commands:
        command: str = command.format(xx="CA")
        os.system(command)


if __name__ == "__main__":
    main()

### END ###
