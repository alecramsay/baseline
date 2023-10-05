#!/usr/bin/env python3

"""
TYPES
"""

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


### END ###
