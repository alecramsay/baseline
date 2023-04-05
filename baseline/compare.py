#!/usr/bin/env python3

"""
COMPARE CANDIDATE BASELINE MAPS
"""

from pyutils import FileSpec

from .constants import districts_by_state
from .baseline import label_iteration


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


### END ###
