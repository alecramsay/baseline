#!/usr/bin/env python3

"""
COMPARE CANDIDATE BASELINE MAPS
"""

from pyutils import FileSpec


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
    rhs: list[str]
    name: str = "N/A"
    qualifier: str
    energy: float
    contiguous: bool = False
    popdev: float = 100.0

    for line in lines:
        if line.startswith("Map "):
            result = line[4:].strip()
            parts = [x.strip() for x in result.split("=")]

            name = parts[0]
            qualifier = parts[1].split(" ")[0]
            if qualifier in ["Contiguous", "Discontiguous"]:
                # Map NC20C_I000K01N14 = Contiguous 14
                # Map NC20C_I018K01N14 = Discontiguous 15 != 14
                contiguous = True if qualifier == "Contiguous" else False
            else:
                # Map NC20C_I000K01N14 = 740980 to 751329, Diff = 10349, Percent = 1.388%
                popdev = float(parts[-1].strip("%")) / 100

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

            plans[name] = {
                "MAP": name,
                "ENERGY": energy,
                "CONTIGUOUS": contiguous,
                "POPDEV": popdev,
            }

            continue

    return plans


def find_best_plan(
    plans: dict[str, dict],
) -> str:
    """Find the lowest energy contiguous plan with 'roughly equal' populations."""

    best_plan_name: str = "TBD"
    lowest_energy: float = 1e9

    for k, v in plans.items():
        if (
            (v["ENERGY"] < lowest_energy)
            and (v["CONTIGUOUS"] is True)
            and (v["POPDEV"] <= 0.02)
        ):
            lowest_energy = v["ENERGY"]
            best_plan_name = v["MAP"]

    return best_plan_name


### END ###
