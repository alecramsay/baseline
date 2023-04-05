#!/usr/bin/env python3

"""
COMPARE CANDIDATE BASELINE MAPS
"""

from pyutils import FileSpec

from .constants import districts_by_state
from .baseline import label_iteration
from .datatypes import Plan
from .coi import uncertainty_of_membership, effective_splits


def cull_energies(log_txt: str, xx: str, plan_type: str) -> list[dict]:
    """Cull plan (map) energies from a log file."""

    abs_path: str = FileSpec(log_txt).abs_path
    with open(abs_path, "r") as f:
        lines: list[str] = list()
        line: str = f.readline()
        while line:
            lines.append(line)

            line = f.readline()

    plans: list[dict] = list()
    i: int = 0
    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # district multiplier

    result: str
    parts: list[str]
    name: str = "N/A"
    energy: float
    contiguous: bool = False

    for line in lines:
        if line.startswith("Map "):
            # Map NC20C_I000K01N14 = Contiguous 14
            # Map NC20C_I018K01N14 = Discontiguous 15 != 14
            result = line[4:].strip()
            parts = [x.strip() for x in result.split("=")]

            name = label_iteration(i, K, N)  # parts[0]
            contiguous = True if parts[1].split(" ")[0] == "Contiguous" else False

            continue

        if line.startswith("Energy for map "):
            # Energy for map NC20C_I000K01N14 = 3100302.685077957

            result = line[15:].strip()
            parts = [x.strip() for x in result.split("=")]

            again: str = label_iteration(i, K, N)  # parts[0]
            if again != name:
                raise ValueError(f"Unexpected map name: {name} != {again}")

            energy = float(parts[1])

            plans.append({"MAP": name, "ENERGY": energy, "CONTIGUOUS": contiguous})

            i += 1
            continue

    return plans


def find_lowest_energies(
    plans: list[dict],
) -> tuple[dict[str, str], dict[str, float]]:
    """Find the lowest energy plans for 1-10, 1-100, and 1-1000 runs."""

    lowest_energy: dict[str, float] = {"ten": 1e9, "hundred": 1e9, "thousand": 1e9}
    lowest_plans: dict[str, str] = {
        "ten": "TBD",
        "hundred": "TBD",
        "thousand": "TBD",
    }

    for i, plan in enumerate(plans):
        if i < 10 and plan["ENERGY"] < lowest_energy["ten"]:
            lowest_energy["ten"] = plan["ENERGY"]
            lowest_plans["ten"] = plan["MAP"]

        if i < 100 and plan["ENERGY"] < lowest_energy["hundred"]:
            lowest_energy["hundred"] = plan["ENERGY"]
            lowest_plans["hundred"] = plan["MAP"]

        if i < 1000 and plan["ENERGY"] < lowest_energy["thousand"]:
            lowest_energy["thousand"] = plan["ENERGY"]
            lowest_plans["thousand"] = plan["MAP"]

    return lowest_plans, lowest_energy


class PlanDiff:
    """Compute 'splits' for the districts of two plans."""

    splits: list[list[float]]
    uncertainty_by_district: list[float]
    splits_by_district: list[float]

    def __init__(self, base: Plan, compare: Plan) -> None:
        self._compute_splits(base, compare)

    def _compute_splits(self, base: Plan, compare: Plan) -> None:
        plan_splits: list[list[float]] = list()

        for i in base.district_ids:
            district_splits: list[float] = list()
            base_geoids: set[str] = base.geoids_for_district(i)

            for j in compare.district_ids:
                compare_geoids: set[str] = compare.geoids_for_district(j)
                intersection: set[str] = base_geoids.intersection(compare_geoids)

                if intersection:
                    # districts: list[int] = [from_id, to_id]
                    # n: int = len(intersection)
                    # pop: int = 0
                    # for geoid in intersection:
                    #     n += 1
                    #     pop += features[geoid].pop
                    # region: Region = Region(
                    #     districts=districts,
                    #     geoids=intersection,
                    #     n=n,
                    #     pop=pop,
                    # )
                    # district_splits.append(region)

                    continue  # TODO: remove

        self.splits = [[0.33, 0.33, 0.34], [0.92, 0.05, 0.03]]


### END ###
