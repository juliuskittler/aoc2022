import copy
import pathlib
import string
from typing import Dict, List, Optional, Tuple

"""
Note: 
- Similar to the previous solution but this time we traverse from E to an "a" node.
- From all available "a" nodes we have to pick the node that results in the shortest
possible path from E to the respective "a" node.
- The "a" node that we choose is simply the first "a" node from our "prev" array.
"""


def get_distance(letter_next: str, letter_curr: str) -> int:
    """Auxilary function to get the distance between 2 letters.

    Here the distance is defined as the number of 'letter steps'
    you have to take in order to move from one letter to another.
    E.g. from 'a' to 'b', it's one step (1), from 'b' to 'a' it's
    one step back (-1), from 'a' to 'c' it's two steps (2), from
    'c' to 'a' it's two steps back (-2) etc.
    """
    # E has the elevation of z, S has the elevation of a
    if letter_next == "E":
        letter_next = "z"
    elif letter_next == "S":
        letter_next = "a"
    if letter_curr == "S":
        letter_curr = "a"
    elif letter_curr == "E":
        letter_curr = "z"

    # Compute the distance
    letter_idx_next = string.ascii_lowercase.index(letter_next)
    letter_idx_curr = string.ascii_lowercase.index(letter_curr)
    distance = letter_idx_next - letter_idx_curr
    return distance


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


def bfs_solve(
    start_node: Tuple[int], graph: Dict[Tuple[int], List[Tuple[int]]]
) -> dict:
    # Initialize useful variables
    queue = [start_node]
    visited = {node: False for node in graph.keys()}
    prev = {
        node: None for node in graph.keys()
    }  # will help us reconstruct the shortest path
    iter = 0

    # Traverse the graph until all nodes are visited
    while len(queue) > 0:
        # Remove the first element from the queu
        node = queue[0]
        queue = queue[1:]

        # Get the neighbors of the current node
        neighbors = graph[node]

        # Loop over each unvisited node
        for neighbor in neighbors:
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True

                prev[neighbor] = {"iter": iter, "node": node}
                iter += 1

    return prev


def bfs_reconstruct(start_node: Tuple[int], end_node: Tuple[int], prev: dict):
    # Reconstruct path going backwards from end node
    current_node = end_node
    path = [current_node]
    while current_node is not start_node:
        current_node = prev[current_node]["node"]
        path.append(current_node)
    path.reverse()
    return path


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
    prev = bfs_solve(e_coord, graph)

    # Identify the "a" node that was visited first
    a_candidates = dict()
    for node in graph:
        i, j = node
        if heightmap[i][j] == "a" and prev[node] is not None:
            a_candidates[prev[node]["iter"]] = node

    first_a_node_iter = min(a_candidates.keys())
    first_a_node = a_candidates[first_a_node_iter]

    # Reconstruct the path to this "a" node
    path = bfs_reconstruct(e_coord, first_a_node, prev)

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
