import copy
import pathlib
from typing import List, Tuple

from utils import BreadthFirstSearch, get_distance

"""
Note: 
- We assume that at any location (with the exception of S), there are at most 3
different directions we can go to because we won't go back to the direction which
we came from.
- The challenge here is: If there are multiple possibilities, how do we know which one
is going to be faster? It seems impossible to tell up-front.
- One possible approach is to use recursion and simply try out all possibilities. E.g.
we can create a function that returns the number of steps required to reach E from a 
given position. For each possible direction (i.e. where the letter is either smaller
or 1 letter larger than the letter of the current direction), the function will call
itself to get the required number of steps for the respective direction. Then, it will
take the minimum of all the returned numbers of steps. However, this seems very 
inefficient because we would visit certain positions multiple times.
- Let's use BFS! Reference: https://www.youtube.com/watch?v=oDqjPvD54Ss
"""


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
    if i > 0 and get_distance(heightmap[i - 1][j], node_letter) <= 1:  # Go up
        candidate_up_coord = (i - 1, j)
        edge_coords.append(candidate_up_coord)
    if i < n - 1 and get_distance(heightmap[i + 1][j], node_letter) <= 1:  # Go down
        candidate_down_coord = (i + 1, j)
        edge_coords.append(candidate_down_coord)
    if j > 0 and get_distance(heightmap[i][j - 1], node_letter) <= 1:  # Go left
        candidate_left_coord = (i, j - 1)
        edge_coords.append(candidate_left_coord)
    if j < m - 1 and get_distance(heightmap[i][j + 1], node_letter) <= 1:  # Go right
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
    bfs.solve(s_coord)
    path = bfs.reconstruct_path(s_coord, e_coord)

    # Compute the minimum number of steps as the length of the path minus 1
    # (minus 1 because we don't count the start step itself)
    min_steps = len(path) - 1
    return min_steps


if __name__ == "__main__":

    filepath = pathlib.Path("12/input.txt")
    with open(filepath, "r") as f:
        heightmap = f.read().splitlines()

    print(solution(heightmap))  # correct: 370

    # Test 1
    heightmap_test = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]
    expected = 31
    assert solution(heightmap_test) == expected
