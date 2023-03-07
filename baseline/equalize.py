#!/usr/bin/env python3

"""
EQUALIZE - Spread out overages to neighbors with underages
"""


def spread_out_overages(deviations: dict, g: dict, verbose: bool = False) -> dict:
    """Spread out overages to neighbors with underages"""

    mods: list = list()

    total_deviation: int = 0
    for k, v in deviations.items():
        total_deviation += abs(v)

    average_deviation: int = int(total_deviation / len(deviations))

    if verbose:
        print("Before:")
        print(f"  {', '.join([f'{k}: {v}' for k, v in deviations.items()])}")
        print(f"  Average = {average_deviation} | total = {total_deviation}")

    after: dict = dict(deviations)  # Update this after each move

    overs: list = [k for k, v in deviations.items() if v > 0]
    overs.sort(key=lambda x: deviations[x], reverse=True)

    for d in overs:
        unders: list = [
            k for k, v in after.items() if v < 0
        ]  # Recompute for each over district
        neighbors: list[int] = list(
            set(g[d]).intersection(unders)
        )  # Only consider "under" neighbors

        total_need: int = sum([abs(after[n]) for n in neighbors])

        if after[d] > total_need:
            # The "over" district can zero out all its "under" neighbors
            for n in neighbors:
                move: int = abs(after[n])
                after[n] += move
                mod: dict = {
                    "from": d,
                    "to": n,
                    "adjustment": move,
                }
                mods.append(mod)
            after[d] = after[d] - total_need

        else:
            # Spread the overage out among the neighbors on a pro rata basis
            moved: int = 0
            for n in neighbors:
                move: int = round(after[d] * abs(after[n]) / total_need)
                moved += move
                after[n] += move
                mod: dict = {
                    "from": d,
                    "to": n,
                    "adjustment": move,
                }
                mods.append(mod)
            after[d] -= moved

    total_deviation: int = 0
    for k, v in after.items():
        total_deviation += abs(v)

    average_deviation: int = int(total_deviation / len(after))

    if verbose:
        print("After:")
        print(f"  {', '.join([f'{k}: {v}' for k, v in after.items()])}")
        print(f"  Average = {average_deviation} | total = {total_deviation}")

    return mods


### END ###
