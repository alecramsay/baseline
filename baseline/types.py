#!/usr/bin/env python3
#
# TYPES
#


from typing import NamedTuple, TypedDict

from .settings import *


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


class District(TypedDict):
    # id: int
    xy: Coordinate
    pop: int
    over_under: int  # over = -, under = +
    stretch: int
    steps: int

    # For intermediate calculations
    sum_xy: Coordinate


class Assignment(TypedDict):
    GEOID: str
    DISTRICT: int
