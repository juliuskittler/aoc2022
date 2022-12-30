"""2022, day 12, part 2: https://adventofcode.com/2022/day/12.

- Similar to the previous solution but this time we traverse from E to an "a" node.
- From all available "a" nodes we have to pick the node that results in the shortest
possible path from E to the respective "a" node.
- The "a" node that we choose is simply the first "a" node from our "prev" array.
"""

import copy
import pathlib
from typing import List, Tuple

from utils import BreadthFirstSearch, get_distance


def get_edge_coords(
    node: Tuple[int],
    heightmap: List[str],
    m: int,
    n: int,
) -> List[Tuple[int]]:

    # Prepare useful variables
    i, j = node
    node_letter = heightmap[i][j]

    # Get next positions
    edge_coords = list()
    if i > 0 and get_distance(heightmap[i - 1][j], node_letter) >= -1:  # Go up
        candidate_up_coord = (i - 1, j)
        edge_coords.append(candidate_up_coord)
    if i < n - 1 and get_distance(heightmap[i + 1][j], node_letter) >= -1:  # Go down
        candidate_down_coord = (i + 1, j)
        edge_coords.append(candidate_down_coord)
    if j > 0 and get_distance(heightmap[i][j - 1], node_letter) >= -1:  # Go left
        candidate_left_coord = (i, j - 1)
        edge_coords.append(candidate_left_coord)
    if j < m - 1 and get_distance(heightmap[i][j + 1], node_letter) >= -1:  # Go right
        candidate_right_coord = (i, j + 1)
        edge_coords.append(candidate_right_coord)

    return edge_coords


def solution(heightmap: List[str]) -> int:
    heightmap = copy.deepcopy(heightmap)

    # Initialize useful variables
    n = len(heightmap)  # number of rows
    m = len(heightmap[0])  # number of columns

    # Identify position of S and E
    for i in range(n):
        for j in range(m):
            if heightmap[i][j] == "S":
                s_coord = (i, j)
            elif heightmap[i][j] == "E":
                e_coord = (i, j)

    # Construct graph for BFS: for each position (node) we get a list of next positions
    # that represent our paths (edges).
    graph = dict()
    for i in range(n):
        for j in range(m):
            node = (i, j)
            graph[node] = get_edge_coords(node, heightmap, m, n)

    # Conduct BFS
    bfs = BreadthFirstSearch(graph)
    bfs.solve(e_coord)

    # Identify the "a" node that was visited first
    a_candidates = dict()
    for node in graph:
        i, j = node
        if heightmap[i][j] == "a" and bfs.previous[node] is not None:
            a_candidates[bfs.iter[node]] = node

    first_a_node_iter = min(a_candidates.keys())
    first_a_node = a_candidates[first_a_node_iter]

    # Reconstruct the path to this "a" node
    path = bfs.reconstruct_path(e_coord, first_a_node)

    # Compute the minimum number of steps as the length of the path minus 1
    # (minus 1 because we don't count the start step itself)
    min_steps = len(path) - 1
    return min_steps


if __name__ == "__main__":

    filepath = pathlib.Path("12/input.txt")
    with open(filepath, "r") as f:
        heightmap = f.read().splitlines()

    print(solution(heightmap))  # correct: 363

    # Test 1
    heightmap_test = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]
    expected = 29
    assert solution(heightmap_test) == expected
