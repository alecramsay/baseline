#!/usr/bin/env python3

"""
TYPES
"""


from typing import NamedTuple, TypedDict


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


### END ###
