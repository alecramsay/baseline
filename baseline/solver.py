#!/usr/bin/env python3
#
# DISTRICT SOLVER
#

import math
import itertools

from .settings import *
from .readwrite import *
from .data import *
from .utils import *
from .helpers import *


class DistrictSolver:
    def __init__(self, settings: dict[str, Any], verbose=False) -> None:
        i: int = self._path_index(settings["units"])
        features_path: str = settings["features_paths"][i]
        self.fc: FeatureCollection = FeatureCollection(features_path)

        self.state: State = State(settings["state_path"])
        self.state.ndistricts: int = settings["districts"]
        self.plan_csv: str = settings["plan_path"]

        self.thresholds: list[float] = settings["thresholds"]
        self.min_threshold: float = self.thresholds[-1]
        self.max_step: int = settings["max_step"]
        self.stretchiness: float = settings["stretchiness"]

        self.verbose: bool = verbose

        self._preprocess_data()
        self.min_tolerance: int = int(self.state.target_pop * self.min_threshold)
        self._setup_districts()
        self._set_max_stretch()

    ### INITIALIZATION METHODS ###

    def _path_index(self, units: str) -> str:
        path_mapping: dict[str, int] = {"tract": 0, "bg": 1, "block": 2}
        path_index: int = path_mapping[units]

        return path_index

    def _preprocess_data(self) -> None:
        self.state.target_pop: int = round(self.fc.total_pop / self.state.ndistricts)

        if self.verbose:
            print(f"Target district population: {self.state.target_pop}")

        self.fc.check_feature_sizes(self.state.ndistricts)

    def _setup_districts(self) -> None:
        self.dc: DistrictCollection = DistrictCollection(
            self.state.ndistricts, self.max_step
        )
        self.dc.seed_districts(self.state, self.verbose)

    def _set_max_stretch(self) -> None:
        """
        The most that will be added to / subtracted from distances to form districts.
        """

        bbox_area: float = (self.state.xmax - self.state.xmin) * (
            self.state.ymax - self.state.ymin
        )
        coverage: float = 0.75
        state_area_est: float = bbox_area * coverage  # degress^2

        district_radius: float = math.sqrt(
            (state_area_est / self.state.ndistricts) / math.pi
        )

        # Stretch in degrees
        max_stretch: float = district_radius * self.stretchiness

        # Stretch normalized to the bitwise stretch steps
        self.rel_stretch: float = max_stretch / self.max_step

        if self.verbose:
            print(
                "max_stretch: {:6f} degrees".format(max_stretch),
                "|",
                "rel_stretch: {:6f} km".format(max_stretch * M_PER_DEG / 1000),
            )
            print()

        return

    ### SOLVER METHODS ###

    @Timer.time_method
    def minimize_district_moi(self) -> bool:
        districts: list[District] = self.dc.districts
        features: list[Feature] = self.fc.features

        for n, t in enumerate(self.thresholds):
            self.tolerance: int = int(self.state.target_pop * t)

            """
            The first time through, compute district populations using the initial seeds.
            After each iteration, recompute the populations using the new district centers.
            """

            self._compute_populations()

            if all(
                [
                    within_tolerance(
                        districts[i]["pop"] - self.state.target_pop,
                        self.min_tolerance,
                    )
                    for i in range(1, self.state.ndistricts + 1)
                ]
            ):
                print()
                print(
                    "All districts within tolerance before iteration {}.".format(n + 1)
                )
                print()

                break

            """
            Find the best districts for a set of given centers, by converging on a
            set of stretch factors that modify distances and bring district populations
            within tolerance.
            """

            if not self.stretch_districts(n + 1):
                print("Failure to converge at iteration", n + 1)
                return False

            """
            # Find the best centers for the given districts, (re)locating the center
            # of each district at its population center of mass.
            """

            # Re-initialize the district (x,y) aggregates
            for i in range(1, self.state.ndistricts + 1):
                districts[i]["sum_xy"] = Coordinate(0, 0)

            for feature in features:
                # geoid: str = feature["geoid"]
                d: int = feature["district"]
                pop: int = feature["pop"]
                xy: Coordinate = feature["xy"]

                dx: float = pop * xy.x
                dy: float = pop * xy.y

                sum_xy: Coordinate = districts[d]["sum_xy"]
                districts[d]["sum_xy"] = Coordinate(sum_xy.x + dx, sum_xy.y + dy)

            for d in range(1, self.state.ndistricts + 1):
                xy: Coordinate = Coordinate(
                    districts[d]["sum_xy"].x / districts[d]["pop"],
                    districts[d]["sum_xy"].y / districts[d]["pop"],
                )
                districts[d]["xy"] = xy

            pass  # Iterate

        if self.verbose:
            print()
            print("Final population deviation: {0:6.2%}".format(self.pop_dev))
            for d in range(1, self.state.ndistricts + 1):
                print("District", d, "size is", districts[d]["pop"])
            print()

        return True  # Districts w/in final population tolerance!

    def stretch_districts(self, n: int) -> bool:
        """
        Find the best districts for a set of given centers, by converging on a
        set of stretch factors that modify distances and bring district populations
        within tolerance.
        """

        districts: list[District] = self.dc.districts

        # NOTE - This is a key decision: Don't reduce the max stretch step w/ each iteration.

        # Re-initialize the stretch steps & district over/unders
        for i in range(1, self.state.ndistricts + 1):
            districts[i]["steps"] = self.max_step

        # Loop until all districts are within tolerance.
        for j in itertools.count(start=1):

            # (1) Make the most populous district have fewer people.

            converged: bool = True
            most_delta: int = MAX_INT
            most_index: int = 0

            for i in range(1, self.state.ndistricts + 1):
                # '-' values mean extra people; '+' values mean not enough people
                districts[i]["over_under"] = self.state.target_pop - districts[i]["pop"]

                # The district with the smallest diff has the most people.
                # The diff must be negative.
                if districts[i]["over_under"] < most_delta:
                    most_delta = districts[i]["over_under"]
                    most_index = i

                if not self._within_tolerance(i):
                    converged = False

            if converged:
                return True

            if not districts[most_index]["steps"]:
                return False

            # Stretch the district with the most people in "in" / less, i.e. shrink it.
            districts[most_index]["stretch"] -= districts[most_index]["steps"]

            self._compute_populations()

            # If the stretched (shrunken) district overshoots by too much, reverse the change.
            while (districts[most_index]["pop"] - self.state.target_pop) < most_delta:
                districts[most_index]["steps"] >>= 1
                # Added this guard
                if not districts[most_index]["steps"]:
                    return False
                districts[most_index]["stretch"] += districts[most_index]["steps"]
                self._compute_populations()

            # If the stretched (shrunken) district overshoots the target population,
            # reduce the stretch step size.
            if districts[most_index]["pop"] < self.state.target_pop:
                districts[most_index]["steps"] >>= 1

            # (2) Make the least populous district have more people.

            converged: bool = True
            least_delta: int = MIN_INT
            least_index: int = 0

            for i in range(1, self.state.ndistricts + 1):
                # '-' values mean extra people; '+' values mean not enough people
                districts[i]["over_under"] = self.state.target_pop - districts[i]["pop"]

                # The district with the biggest diff has the fewest people.
                # The diff must be positive.
                if districts[i]["over_under"] > least_delta:
                    least_delta = districts[i]["over_under"]
                    least_index = i

                if not self._within_tolerance(i):
                    converged = False

            if converged:
                return True

            if not districts[least_index]["steps"]:
                return False

            # Stretch the district with the fewest people "out" / more, i.e., expand it.
            districts[least_index]["stretch"] += districts[least_index]["steps"]

            self._compute_populations()

            # If the stretched (expanded) district overshoots by too much, reverse the change.
            while (districts[least_index]["pop"] - self.state.target_pop) > least_delta:
                districts[least_index]["steps"] >>= 1
                # Added this guard
                if not districts[least_index]["steps"]:
                    return False
                districts[least_index]["stretch"] -= districts[least_index]["steps"]
                self._compute_populations()

            # If the stretched (expanded) district overshoots the target population,
            # reduce the stretch step size.
            if districts[least_index]["pop"] > self.state.target_pop:
                districts[least_index]["steps"] >>= 1

            self._log_intermediate_state(n, j)

    ### HOUSEKEEPING METHODS ###

    def write_plan(self) -> None:
        write_csv(self.plan_csv, self.plan, ["GEOID20", "DISTRICT"])

    ### HELPER METHODS ###

    def _compute_populations(self) -> None:
        districts: list[District] = self.dc.districts
        features: list[Feature] = self.fc.features

        # Re-initialize the district populations
        for i in range(1, self.state.ndistricts + 1):
            districts[i]["pop"] = 0

        # Cache district assignments & list of dicts for writing it to a CSV file.
        self.plan: list = list()

        for i, feature in enumerate(features):
            geoID: str = feature["geoid"]
            prev: int = feature["district"]
            pt: Coordinate = feature["xy"]
            pop: int = feature["pop"]

            next: int = self._closest_district(pt)

            districts[next]["pop"] += pop
            feature["district"] = next

            row: dict[str, int] = {"GEOID20": geoID, "DISTRICT": next}
            self.plan.append(row)

        pops: list[int] = [x["pop"] for x in districts[1:]]
        self.pop_dev: float = population_deviation(pops, self.state.target_pop)

    def _closest_district(self, fPt: Coordinate) -> int:
        """
        Checks every district every time.
        """
        imin: int = 1
        dmin: float = self._distance_to(fPt, imin)

        for i in range(2, self.state.ndistricts + 1):
            d: float = self._distance_to(fPt, i)
            if d < dmin:
                imin = i
                dmin = d

        return imin

    def _distance_to(self, fPt: Coordinate, d: int) -> float:
        districts: list[District] = self.dc.districts

        dPt: Coordinate = districts[d]["xy"]
        stretch: float = self.rel_stretch * districts[d]["stretch"]
        distance: float = stretched_distance(fPt, dPt, stretch)

        return distance

    def _within_tolerance(self, i: int) -> bool:
        districts: list[District] = self.dc.districts

        return within_tolerance(districts[i]["over_under"], self.tolerance)

    def _log_intermediate_state(self, n: int, j: int) -> None:
        if self.verbose:
            print(
                "{:2} / {:4}".format(n, j),
                "- dev: {0:6.2%}".format(self.pop_dev),
                "threshold: {0:6.3%}".format(self.tolerance / self.state.target_pop),
            )


### HELPER FUNCTIONS ###


def distance(pt1: Coordinate, pt2: Coordinate) -> float:
    """
    Compute a distance between two points, using a Cartesian (flat earth) not
    geodesic (curved earth) model.
    """

    dx: float = pt1.x - pt2.x
    dy: float = pt1.y - pt2.y

    d: float = math.sqrt(dx**2 + dy**2)

    return d


def stretched_distance(pt1: Coordinate, pt2: Coordinate, stretch: float) -> float:
    """
    Compute a distance between two points, incorporating a "stretch" factor and
    using a Cartesian (flat earth) not geodesic (curved earth) model. Because of
    the stretching, distances can be negative. Features with negative distances
    are the closest to the district center.
    """

    dx: float = pt1.x - pt2.x
    dy: float = pt1.y - pt2.y

    d: float = math.sqrt(dx**2 + dy**2) - stretch

    return d


# LIMIT WHAT GETS EXPORTED.


__all__: list[str] = ["DistrictSolver"]
