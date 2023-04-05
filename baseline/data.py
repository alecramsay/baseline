#!/usr/bin/env python3

"""
DATA STRUCTURES
"""

from shapely.geometry import Point, Polygon, MultiPolygon

from .readwrite import *
from .datatypes import Feature

# from .plastic import *


class FeatureCollection:
    """
    Collections of geographic features: precincts (VTDs), tracts, BGs, blocks.
    """

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
        """
        Warn if any features are more populous than a target district.
        """

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


### END ###
