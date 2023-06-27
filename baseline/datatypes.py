#!/usr/bin/env python3

"""
TYPES
"""

from collections import defaultdict
from typing import NamedTuple, TypedDict

from .readwrite import read_csv


class Coordinate(NamedTuple):
    x: float
    y: float

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Feature(TypedDict):
    geoid: str
    xy: Coordinate
    pop: int
    district: int


class GeoID:
    """
    Parse 15-character GeoIDs into their component parts.
    """

    def __init__(self, id: str) -> None:
        self.state: str = id[0:2]
        self.county: str = id[0:5]  # id[2:5]
        self.tract: str = id[0:11]  # id[5:11]
        self.bg: str = id[0:12]  # id[11:12]
        self.block: str = id  # id[12:15]


class Plan:
    _district_ids: set[int]
    _district_by_geoid: dict[str, int]
    _geoids_by_district: dict[int, set[str]]
    _pop_by_district: dict[int, int]
    _pop_by_geoid: dict[str, int]

    def __init__(self, rel_path: str, pop_by_geoid: dict[str, int]) -> None:
        assignments: list[dict] = read_csv(rel_path, [str, int])
        self._district_by_geoid = {
            str(row["GEOID"]): row["DISTRICT"] for row in assignments
        }
        self._pop_by_geoid = pop_by_geoid

        self._invert()
        self._district_ids = set(self._geoids_by_district.keys())

        self._sum_pop_by_district()

    def _invert(self) -> None:
        self._geoids_by_district = defaultdict(set)
        for geoid, district in self._district_by_geoid.items():
            self._geoids_by_district[district].add(geoid)

    def _sum_pop_by_district(self) -> None:
        self._pop_by_district = defaultdict(int)
        for district, geoids in self._geoids_by_district.items():
            for geoid in geoids:
                if geoid in self._pop_by_geoid:
                    self._pop_by_district[district] += self._pop_by_geoid[geoid]

    @property
    def district_ids(self) -> set[int]:
        return self._district_ids

    def district_for_geoid(self, geoid: str) -> int:
        return self._district_by_geoid[geoid]

    def geoids_for_district(self, district: int) -> set[str]:
        return self._geoids_by_district[district]

    def population_for_district(self, district: int) -> int:
        return self._pop_by_district[district]

    def population_for_split(self, geoids: set[str]) -> int:
        pop: int = 0
        for geoid in geoids:
            if geoid in self._pop_by_geoid:
                pop += self._pop_by_geoid[geoid]

        return pop


### END ###
