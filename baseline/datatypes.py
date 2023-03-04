#!/usr/bin/env python3

"""
TYPES
"""


from typing import NamedTuple, TypedDict

# from typing import Self


class Coordinate(NamedTuple):
    x: int
    y: int

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


### END ###
