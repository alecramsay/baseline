#!/usr/bin/env python3

"""
Test evening out adjacent districts' over/under populations
"""

from baseline import *


# def spread_out_overages(deviations: dict, g: dict, verbose: bool = False) -> dict:
#     """Spread out overages to neighbors with underages"""

#     mods: list = list()

#     total_deviation: int = 0
#     for k, v in deviations.items():
#         total_deviation += abs(v)

#     average_deviation: int = int(total_deviation / len(deviations))

#     if verbose:
#         print("Before:")
#         print(f"  {', '.join([f'{k}: {v}' for k, v in deviations.items()])}")
#         print(f"  Average = {average_deviation} | total = {total_deviation}")

#     after: dict = dict(deviations)  # Update this after each move

#     overs: list = [k for k, v in deviations.items() if v > 0]
#     overs.sort(key=lambda x: deviations[x], reverse=True)

#     for d in overs:
#         unders: list = [
#             k for k, v in after.items() if v < 0
#         ]  # Recompute for each over district
#         neighbors: list[int] = list(
#             set(g[d]).intersection(unders)
#         )  # Only consider "under" neighbors

#         total_need: int = sum([abs(after[n]) for n in neighbors])

#         if after[d] > total_need:
#             # The "over" district can zero out all its "under" neighbors
#             for n in neighbors:
#                 move: int = abs(after[n])
#                 after[n] += move
#                 mod: dict = {
#                     "from": d,
#                     "to": n,
#                     "adjustment": move,
#                 }
#                 mods.append(mod)
#             after[d] = after[d] - total_need

#         else:
#             # Spread the overage out among the neighbors on a pro rata basis
#             moved: int = 0
#             for n in neighbors:
#                 move: int = round(after[d] * abs(after[n]) / total_need)
#                 moved += move
#                 after[n] += move
#                 mod: dict = {
#                     "from": d,
#                     "to": n,
#                     "adjustment": move,
#                 }
#                 mods.append(mod)
#             after[d] -= moved

#     total_deviation: int = 0
#     for k, v in after.items():
#         total_deviation += abs(v)

#     average_deviation: int = int(total_deviation / len(after))

#     if verbose:
#         print("After:")
#         print(f"  {', '.join([f'{k}: {v}' for k, v in after.items()])}")
#         print(f"  Average = {average_deviation} | total = {total_deviation}")

#     return mods


def main() -> None:
    verbose: bool = True

    g: dict = {
        1: [8, 12],
        2: [3, 8],
        3: [2, 8, 10, 13, 14],
        4: [5, 6, 7, 10, 13],
        5: [4, 6, 11, 13],
        6: [4, 5, 7, 9, 11],
        7: [4, 6, 9, 10],
        8: [1, 2, 3, 10, 12],
        9: [6, 7, 10, 11, 14],
        10: [3, 4, 7, 8, 9, 12, 13],
        11: [5, 6, 9, 13, 14],
        12: [1, 8, 10],
        13: [3, 4, 5, 10, 11, 14],
        14: [3, 9, 11, 13],
    }  # GA

    # Check consistency of graph
    consistent: bool = True
    for node, neighbors in g.items():
        for neighbor in neighbors:
            if node not in g[neighbor]:
                consistent = False
                print(f"ERROR: {node} not in {neighbor}'s neighbors")
    if consistent:
        print("Graph is consistent")

    deviations: dict = {
        1: 161,
        2: 4392,
        3: -1193,
        4: 4164,
        5: -1809,
        6: 2118,
        7: -2211,
        8: -1846,
        9: 816,
        10: -1102,
        11: 589,
        12: -461,
        13: -1621,
        14: -1993,
    }

    moves: dict = spread_out_overages(deviations, g, verbose)

    for m in moves:
        print(f"Move {m['adjustment']} from {m['from']} to {m['to']}")

    pass


if __name__ == "__main__":
    main()

### END ###
