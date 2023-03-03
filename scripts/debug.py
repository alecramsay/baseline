#!/usr/bin/env python3

"""
DEBUG

https://www.baeldung.com/cs/shortest-path-visiting-all-nodes
https://www.graphable.ai/blog/best-graph-traversal-algorithms/
https://en.wikipedia.org/wiki/Shortest_path_problem#Unweighted_graphs

https://www.cs.cornell.edu/courses/cs2112/2012sp/lectures/lec24/lec24-12sp.html
https://www.programiz.com/dsa/graph-bfs?ref=hackernoon.com
"""

from baseline import *

data: dict = {
    1: [2, 3, 4, 13, "OUT_OF_STATE"],
    2: [9, 4, 13, 1],
    3: [1, 13, 7, "OUT_OF_STATE"],
    4: [9, 2, 6, 1, "OUT_OF_STATE"],
    5: [8, 10, 11, 6, "OUT_OF_STATE"],
    6: [8, 9, 4, 5, "OUT_OF_STATE"],
    7: [9, 3, 13, "OUT_OF_STATE"],
    8: [5, 6, 9, 10, 12, 14, "OUT_OF_STATE"],
    9: [2, 4, 6, 7, 8, 13, "OUT_OF_STATE"],
    10: [5, 8, 11, 12, 14, "OUT_OF_STATE"],
    11: [10, 5, "OUT_OF_STATE"],
    12: [8, 10, 14],
    13: [1, 2, 3, 7, 9],
    14: [8, 10, 12, "OUT_OF_STATE"],
}

g: Graph = Graph(data)

border: list = [OUT_OF_STATE]
outer: list = []
while True:
    ring: list = g.ring(border, outer)
    if len(ring) == 0:
        break

    print(f"ring: {ring}")
    outer += border
    border = ring

    pass

# ring: list = g.ring(["OUT_OF_STATE"])
# ring: list = g.ring(ring)
# for node, neighbors in data.items():
#     if OUT_OF_STATE in neighbors:
#         ring.append(node)

pass

"""
g: dict = {
    1: [2, 3, 4, 13, 'OUT_OF_STATE'],
    2: [9, 4, 13, 1],
    3: [1, 13, 7, 'OUT_OF_STATE'],
    4: [9, 2, 6, 1, 'OUT_OF_STATE'],
    5: [8, 10, 11, 6, 'OUT_OF_STATE'],
    6: [8, 9, 4, 5, 'OUT_OF_STATE'],
    7: [9, 3, 13, 'OUT_OF_STATE'],
    8: [5, 6, 9, 10, 12, 14, 'OUT_OF_STATE'],
    9: [2, 4, 6, 7, 8, 13, 'OUT_OF_STATE'],
    10: [5, 8, 11, 12, 14, 'OUT_OF_STATE'],
    11: [10, 5, 'OUT_OF_STATE'],
    12: [8, 10, 14],
    13: [1, 2, 3, 7, 9],
    14: [8, 10, 12, 'OUT_OF_STATE'],
}
"""

### END ###
