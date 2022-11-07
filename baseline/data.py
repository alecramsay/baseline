#!/usr/bin/env python3
#
# DATA STRUCTURES
#

import random
from collections import namedtuple
from shapely.geometry import Point, Polygon, MultiPolygon
from typing import NamedTuple, TypedDict

from .settings import *
from .io import *
from .types import *
from .plastic import *


class FeatureCollection:
    """
    Collections of tracts, BGs, or blocks.
    """

    def __init__(self, features_path) -> None:
        self.features: list[Feature] = self._load(features_path)
        self.total_pop: int = 0
        self.avg_pop: int = 0

        self._calc_one_time_stats()

    def _load(self, rel_path: str) -> bytes:
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


class State:
    def __init__(self, rel_path) -> None:
        self.shape: Polygon | MultiPolygon = load_state_shape(rel_path, "GEOID20")

        self.xmin: float
        self.ymin: float
        self.xmax: float
        self.ymax: float
        self.xmin, self.ymin, self.xmax, self.ymax = self.shape.bounds

    def contains(self, pt: Point) -> bool:
        return self.shape.contains(pt)


class DistrictCollection:
    """
    A collection of districts.
    """

    def __init__(self, n: int, max_step: int) -> None:
        self.n: int = n
        d: District = {
            "xy": Coordinate(0, 0),
            "pop": 0,
            "over_under": 0,
            "stretch": 0,
            "steps": max_step,
            "sum_xy": Coordinate(0, 0),
        }
        # Districts are referenced by their index in the list.
        # The extra '0' district is 'unassigned'.
        self.districts: list[District] = [dict(d) for i in range(n + 1)]

    def seed_districts(self, state: State, verbose=False) -> None:
        """
        Use a plastic sequence to seed the district centers.
        """

        seeds: list[Coordinate] = PlasticCoordinates(self.n, state.shape).coordinates
        # seeder: PlasticCoordinates = PlasticCoordinates(self.n, state.shape)
        # seeds: list[Coordinate] = seeder.coordinates

        for i in range(1, self.n + 1):  # Skip the '0' district.
            j: int = i - 1

            seed: Coordinate = seeds[j]
            self.districts[i]["xy"] = seed
