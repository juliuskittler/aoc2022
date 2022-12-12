import copy
import pathlib
import string
from typing import List, Optional, Tuple

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
take the minimum of all the returned numbers of steps.
- But can we be smarter? Would it help to work the problem backwards (e.g. from E to S)
or somehow make use of the fact that we know the position of both E and S upfront?
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


def get_min_steps_from_a_to_b(
    a_coord: Tuple[int],
    b_coord: Tuple[int],
    heightmap: List[str],
    n: int,
    m: int,
    steps_taken: int,
    seen_coords: Optional[List[Tuple[int]]] = None,
) -> int:
    """Recursive function to get the minimum number of steps from a to b."""
    # Ensure that steps_taken cannot be adjusted by other function calls
    steps_taken = copy.deepcopy(steps_taken)
    seen_coords = copy.deepcopy(seen_coords)

    # Identify all possible positions where we can go from the a_coord position
    candidate_coords = list()
    i_a, j_a = a_coord
    a_letter = heightmap[i_a][j_a]
    if seen_coords is None:
        seen_coords = list()

    if i_a > 0 and get_distance(heightmap[i_a - 1][j_a], a_letter) >= -1:  # Go up
        candidate_up_coord = (i_a - 1, j_a)
        if candidate_up_coord not in seen_coords:
            candidate_coords.append(candidate_up_coord)
    if i_a < n - 1 and get_distance(heightmap[i_a + 1][j_a], a_letter) >= -1:  # Go down
        candidate_down_coord = (i_a + 1, j_a)
        if candidate_down_coord not in seen_coords:
            candidate_coords.append(candidate_down_coord)
    if j_a > 0 and get_distance(heightmap[i_a][j_a - 1], a_letter) >= -1:  # Go left
        candidate_left_coord = (i_a, j_a - 1)
        if candidate_left_coord not in seen_coords:
            candidate_coords.append(candidate_left_coord)
    if (
        j_a < m - 1 and get_distance(heightmap[i_a][j_a + 1], a_letter) >= -1
    ):  # Go right
        candidate_right_coord = (i_a, j_a + 1)
        if seen_coords is None or candidate_right_coord not in seen_coords:
            candidate_coords.append(candidate_right_coord)

    # # Debug
    # # print("len(seen_coords): {}".format(len(seen_coords)))
    # # print("steps_taken: {}".format(steps_taken))
    # if steps_taken == 1:
    #     print("\n\n\n")
    #     heightmap_copy = copy.deepcopy(heightmap)
    #     heightmap_copy[i_a]= heightmap_copy[i_a][0:j_a] + "." + heightmap_copy[i_a][j_a+1:]
    #     for row in heightmap_copy:
    #         print(row)

    # Check termination conditions:
    # If the target is in the candidate coords, return 1
    if b_coord in candidate_coords:
        return steps_taken + 1
    # If there are not candidates, return a very large number
    elif len(candidate_coords) == 0:
        return 9e10

    # Call get_min_steps_from_a_to_b itself for each possible direction
    candidate_steps = list()
    seen_coords.append(a_coord)
    for cand in candidate_coords:
        n_steps = get_min_steps_from_a_to_b(
            cand, b_coord, heightmap, n, m, steps_taken + 1, seen_coords
        )
        candidate_steps.append(n_steps)

    # Take the minimum of all results and return it
    min_steps = min(candidate_steps)
    return min_steps


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

    # Get minimum number of distance steps between a and b
    steps_taken = 0
    min_steps = get_min_steps_from_a_to_b(
        e_coord, s_coord, heightmap, n, m, steps_taken
    )
    return min_steps


if __name__ == "__main__":

    filepath = pathlib.Path("12/input.txt")
    with open(filepath, "r") as f:
        heightmap = f.read().splitlines()

    print(solution(heightmap))

    # Test 1
    heightmap_test = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]
    expected = 31
    print(solution(heightmap_test))
    # assert solution(heightmap_test) == expected
