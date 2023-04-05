#!/usr/bin/env python3

"""
COMPARE CANDIDATE BASELINE MAPS
"""

from pyutils import FileSpec

from .constants import districts_by_state
from .baseline import label_iteration
from .datatypes import Plan
from .coi import uncertainty_of_membership, effective_splits


# def cull_energies(log_txt: str, xx: str, plan_type: str) -> list[dict]:
def cull_energies(log_txt: str, xx: str, plan_type: str) -> dict[str, dict]:
    """Cull plan (map) energies from a log file."""

    abs_path: str = FileSpec(log_txt).abs_path
    with open(abs_path, "r") as f:
        lines: list[str] = list()
        line: str = f.readline()
        while line:
            lines.append(line)

            line = f.readline()

    plans: dict[str, dict] = dict()

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

            name = parts[0]
            # name = label_iteration(i, K, N)  # parts[0]
            contiguous = True if parts[1].split(" ")[0] == "Contiguous" else False

            continue

        if line.startswith("Energy for map "):
            # Energy for map NC20C_I000K01N14 = 3100302.685077957

            result = line[15:].strip()
            parts = [x.strip() for x in result.split("=")]

            again: str = parts[0]
            # again: str = label_iteration(i, K, N)  # parts[0]
            if again != name:
                raise ValueError(f"Unexpected map name: {name} != {again}")

            energy = float(parts[1])

            plans[name] = {"MAP": name, "ENERGY": energy, "CONTIGUOUS": contiguous}

            continue

    return plans


def find_lowest_energies(
    plans: dict[str, dict],
) -> tuple[dict[str, str], dict[str, float]]:
    """Find the lowest energy plans for 1-10, 1-100, and 1-1000 runs."""

    lowest_energy: dict[str, float] = {"1-10": 1e9, "1-100": 1e9, "1-1000": 1e9}
    lowest_plans: dict[str, str] = {
        "1-10": "TBD",
        "1-100": "TBD",
        "1-1000": "TBD",
    }

    i: int = 0
    for k, v in plans.items():
        if i < 10 and v["ENERGY"] < lowest_energy["1-10"]:
            lowest_energy["1-10"] = v["ENERGY"]
            lowest_plans["1-10"] = v["MAP"]

        if i < 100 and v["ENERGY"] < lowest_energy["1-100"]:
            lowest_energy["1-100"] = v["ENERGY"]
            lowest_plans["1-100"] = v["MAP"]

        if i < 1000 and v["ENERGY"] < lowest_energy["1-1000"]:
            lowest_energy["1-1000"] = v["ENERGY"]
            lowest_plans["1-1000"] = v["MAP"]

        i += 1

    return lowest_plans, lowest_energy


class PlanDiff:
    """Compute 'splits' for the districts of two plans."""

    splits: list[list[float]]
    uom_by_district: list[float]
    es_by_district: list[float]

    def __init__(self, base: Plan, compare: Plan) -> None:
        self._compute_splits(base, compare)
        self._compute_metrics()

    def _compute_splits(self, base: Plan, compare: Plan) -> None:
        plan_splits: list[list[float]] = list()

        for i in base.district_ids:
            district_splits: list[float] = list()
            base_geoids: set[str] = base.geoids_for_district(i)
            base_total: int = base.population_for_district(i)

            for j in compare.district_ids:
                compare_geoids: set[str] = compare.geoids_for_district(j)
                intersection: set[str] = base_geoids.intersection(compare_geoids)

                if intersection:
                    pct: float = base.population_for_split(intersection) / base_total
                    district_splits.append(pct)

            plan_splits.append(district_splits)

        self.splits = plan_splits

    def _compute_metrics(self) -> None:
        self.uom_by_district = list()
        self.es_by_district = list()

        for d in self.splits:
            uom: float = uncertainty_of_membership(d)
            es: float = effective_splits(d)

            self.uom_by_district.append(uom)
            self.es_by_district.append(es)


### END ###
