#!/usr/bin/env python3
"""
Convert pickled data to CSV format.

For example:

$ scripts/unpickle_to_csv.py -s NC -u vtd

For documentation, type:

$ scripts/unpickle_to_csv.py -h

TODO

- Rationalize water-only precincts between data & shapes

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Unpickle data to CSV format."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-u",
        "--unit",
        default="vtd",
        help="The unit of granularity (e.g., vtd)",
        type=str,
    )
    parser.add_argument(
        "-w", "--water", dest="water", action="store_true", help="Water-only precincts"
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Convert pickled data to CSV format."""

    args: Namespace = parse_args()

    xx: str = args.state
    unit: str = args.unit
    if xx in ["OR"]:
        unit = "bg"
    elif xx in ["CA"]:
        unit = "tract"

    water: bool = args.water

    ### DEBUG ###

    ### LOAD DATA ###

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "data"], "_", "pickle"
    )
    collection: FeatureCollection = FeatureCollection(rel_path)

    water_precincts: list = list()
    if water:
        rel_path: str = path_to_file([data_dir, xx]) + file_name(
            [xx, cycle, unit, "water_only"], "_", "csv"
        )  # GEOID,ALAND,AWATER
        types: list = [str, int, int]
        water_precincts = [row["GEOID"] for row in read_csv(rel_path, types)]
        print(f"# of water-only precincts: {len(water_precincts)}")

    ### WRITE DATA AS A CSV ###

    l: list = list()
    for f in collection.features:
        row: dict = {
            "GEOID": f["geoid"],
            "POP": f["pop"],
            "X": f["xy"].x,
            "Y": f["xy"].y,
        }
        if f["geoid"] in water_precincts:
            print(f"Removing water-only precinct {f['geoid']}")
            continue
        else:
            l.append(row)

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "data"], "_", "csv"
    )
    write_csv(rel_path, l, ["GEOID", "POP", "X", "Y"], precision="{:.14f}")


class FeatureCollection:
    """Collections of geographic features: precincts (VTDs), tracts, BGs, blocks."""

    def __init__(self, features_path) -> None:
        self.features: list[Feature] = self._load(features_path)
        self.total_pop: int = 0
        self.avg_pop: int = 0

        self._calc_one_time_stats()

    def _load(self, rel_path: str) -> list[Feature]:
        unpickled: list[Feature] = read_pickle(rel_path)
        if not unpickled:
            raise Exception("Error: FeatureCollection.__init__(): Failed to load data.")

        return unpickled

    def _calc_one_time_stats(self) -> None:
        for i, val in enumerate(self.features):
            self.total_pop += val["pop"]

        self.avg_pop: int = round(self.total_pop / len(self.features))

    def check_feature_sizes(self, ndistricts: int) -> bool:
        """Warn if any features are more populous than a target district."""

        target_pop: int = round(self.total_pop / ndistricts)

        for i, val in enumerate(self.features):
            pop: int = val["pop"]
            if pop > target_pop:
                geoid: str = val["geoid"]

                print()
                print(
                    f"WARNING: Feature {geoid} has more people ({pop}) than the target district size ({target_pop})."
                )
                print()

                return False

        return True

        """
        # Handle features more populous than a single district?
        
        for geoID in self.feature_pop:
            pop = self.feature_pop[geoID]

            fullreps = pop // self.target_pop
            if fullreps > 0:
                print(
                    "Feature {0} has enough people for {1} full districts.".format(
                        geoID, fullreps
                    )
                )
                self.nreps -= fullreps
                self.feature_pop[geoID] -= fullreps * self.target_pop
        """


if __name__ == "__main__":
    main()

### END ###
