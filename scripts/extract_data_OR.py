#!/usr/bin/env python3
#

"""
Preprocess data for OR.

For example:

$ scripts/extract_data_OR.py 
"""

from baseline import *


def main() -> None:
    """Preprocess the block groups for OR."""

    commands: list[str] = [
        "scripts/extract_pop.py -s OR -g -i 3 > data/CA/CA_census_log.txt",
        "scripts/extract_xy.py -s OR -g",
        "scripts/join_feature_data.py -s OR -g",
        "scripts/unpickle_to_csv.py -s OR -u bg",
        "scripts/unpickle_to_csv.py -s OR -u block",
        "scripts/extract_block_bgs.py -s OR",
        "scripts/extract_name_map.py -s OR > data/OR/OR_2020_vtd_names.txt",
    ]
    for command in commands:
        command: str = command.format(xx="CA")
        os.system(command)


if __name__ == "__main__":
    main()

### END ###
