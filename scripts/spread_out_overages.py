#!/usr/bin/env python3

"""
Test evening out adjacent districts' over/under populations
"""

from baseline import *

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

before: dict = {
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

total_deviation: int = 0
for k, v in before.items():
    total_deviation += abs(v)

average_deviation: int = int(total_deviation / len(before))
print(
    f"Before: average deviation = {average_deviation} | total deviation = {total_deviation}"
)

after: dict = dict(before)  # Updated after each swap

overs: list = [k for k, v in before.items() if v > 0]
overs.sort(key=lambda x: before[x], reverse=True)

for d in overs:
    unders: list = [k for k, v in before.items() if v < 0]
    neighbors: list[int] = list(set(g[d]).intersection(unders))

    total_need: int = sum([abs(after[n]) for n in neighbors])

    if before[d] > total_need:
        for n in neighbors:
            after[n] += after[n] * -1
        after[d] = before[d] - total_need

    else:
        for n in neighbors:
            target: int = int(total_need / len(neighbors)) * -1
            delta: int = target - after[n] + int(before[d] / len(neighbors))
            after[n] += delta
        after[d] = 0

total_deviation: int = 0
for k, v in after.items():
    total_deviation += abs(v)

average_deviation: int = int(total_deviation / len(after))
print(
    f"After: average deviation = {average_deviation} | total deviation = {total_deviation}"
)

pass

### END ###
