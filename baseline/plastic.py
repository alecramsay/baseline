#!/usr/bin/env python3
#
# PLASTIC SEQUENCE
# - http://extremelearning.com.au/unreasonable-effectiveness-of-quasirandom-sequences/
# - https://observablehq.com/@jrus/plastic-sequence
#

import math
from shapely.geometry import Point, Polygon, MultiPolygon
from typing import Generator

from .types import Coordinate


class PlasticCoordinates:
    """
    Generate a plastic sequence of coordinates in the shape.
    """

    def __init__(self, n: int, shape: Polygon | MultiPolygon) -> None:
        self.n: int = n
        self.shape: Polygon | MultiPolygon = shape

        xmin: float
        ymin: float
        xmax: float
        ymax: float
        xmin, ymin, xmax, ymax = self.shape.bounds

        self.min_pt: Coordinate
        self.max_pt: Coordinate
        self.min_pt, self.max_pt = trim_bbox(
            Coordinate(xmin, ymin),
            Coordinate(xmax, ymax),
            margin=0.05,
        )

        self.coordinates: list[Coordinate] = []
        self._generate()

    def _generate(self) -> list[Coordinate]:
        gen: Generator[Coordinate, None, None] = plastic_2D_seq()

        for i in range(self.n):
            pt: Coordinate = next(gen)
            seed: Coordinate = rescale_pt(pt, self.min_pt, self.max_pt)

            while not self.shape.contains(Point(seed.x, seed.y)):
                pt: Coordinate = next(gen)
                seed: Coordinate = rescale_pt(pt, self.min_pt, self.max_pt)

            self.coordinates.append(seed)

    def _district_radius(self) -> float:
        bbox_area: float = (self.max_pt.x - self.min_pt.x) * (
            self.max_pt.y - self.min_pt.y
        )
        # How much of the bounding box does the state shape cover?
        coverage: float = 0.75
        state_area_est: float = bbox_area * coverage  # degrees^2

        radius: float = math.sqrt((state_area_est / self.n) / math.pi)

        return radius

    def echo(self) -> str:
        print()
        for seed in self.coordinates:
            print(seed)
        print()
        print("Approximate district radius: {0}".format(self._district_radius()))
        print()


### PLASTIC FUNCTIONS & CONSTANTS ###


def phi(d) -> float:
    """
    The nested radical formula for g=phi(d).
    phi(1) = 1.6180339887498948482
    phi(2) = 1.32471795724474602596
    """
    x: float = 2.0000
    for i in range(10):
        x = pow(1 + x, 1 / (d + 1))

    return x


# g = phi(2)
g: float = 1.32471795724474602596


def plastic_2D_seq() -> Generator[Coordinate, None, None]:
    """
    Generate a 2D plastic sequence.
    """
    alpha: list[float, float] = [0.0, 0.0]

    for j in range(2):
        alpha[j] = pow(1 / g, j + 1) % 1

    seed: float = 0.5
    i: int = 0

    while True:
        x: float = (seed + alpha[0] * (i + 1)) % 1
        y: float = (seed + alpha[1] * (i + 1)) % 1

        i = i + 1

        yield Coordinate(x, y)


### HELPER FUNCTIONS ###


def trim_bbox(
    min_pt: Coordinate, max_pt: Coordinate, margin=0.05
) -> tuple[Coordinate, Coordinate]:
    """
    Trim the bounding box to exclude the margin %.
    """

    new_min_pt: Coordinate = Coordinate(
        min_pt.x + ((max_pt.x - min_pt.x) * margin),
        min_pt.y + ((max_pt.y - min_pt.y) * margin),
    )
    new_max_pt: Coordinate = Coordinate(
        min_pt.x + ((max_pt.x - min_pt.x) * (1 - margin)),
        min_pt.y + ((max_pt.y - min_pt.y) * (1 - margin)),
    )

    return new_min_pt, new_max_pt


def rescale_pt(pt: Coordinate, min_pt: Coordinate, max_pt: Coordinate) -> Coordinate:
    """
    Rescale a unit point -- i.e., x & y in [0, 1] -- within the bounding box.
    """

    x: float = min_pt.x + (max_pt.x - min_pt.x) * pt.x
    y: float = min_pt.y + (max_pt.y - min_pt.y) * pt.y

    return Coordinate(x, y)


### SAMPLE CODE ###

"""
# From http://extremelearning.com.au/unreasonable-effectiveness-of-quasirandom-sequences/

import numpy as np

# Number of dimensions.
d = 2

# number of required points
n = 50

g = phi(d)
alpha = np.zeros(d)
for j in range(d):
    alpha[j] = pow(1 / g, j + 1) % 1
z = np.zeros((n, d))

seed: float = 0.5
for i in range(n):
    z[i] = (seed + alpha * (i + 1)) % 1
print(z)

pass
"""

# LIMIT WHAT GETS EXPORTED.


__all__: list[str] = ["PlasticCoordinates"]
