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


class Pair(NamedTuple):
    one: int
    two: int

    def __repr__(self) -> str:
        return f"{self.one},{self.two}"

    @classmethod
    def from_data(cls, x: int, y: int):  # -> Self:
        one: int = x if x < y else y
        two: int = y if y > x else x

        return cls(one, two)


class Plan:
    _district_by_geoid: dict[str, int]
    _geoids_by_district: dict[int, set[str]]
    _pop_by_district: dict[int, int]

    def __init__(self, rel_path: str, pop_by_geoid: dict[str, int]) -> None:
        assignments: list[dict] = read_csv(rel_path, [str, int])
        self._district_by_geoid = {
            str(row["GEOID"]): row["DISTRICT"] for row in assignments
        }
        self._invert()
        self._sum_pop_by_district(pop_by_geoid)

    def _invert(self) -> None:
        self._geoids_by_district = defaultdict(set)
        for geoid, district in self._district_by_geoid.items():
            self._geoids_by_district[district].add(geoid)

    def _sum_pop_by_district(self, pop_by_geoid: dict[str, int]) -> None:
        self._pop_by_district = defaultdict(int)
        for district, geoids in self._geoids_by_district.items():
            for geoid in geoids:
                self._pop_by_district[district] += pop_by_geoid[geoid]

    def district_for_geoid(self, geoid: str) -> int:
        return self._district_by_geoid[geoid]


### END ###
