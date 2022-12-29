"""2022, day 22, part 1."""
import pathlib
from typing import List, Union

from utils import get_instructions, get_map


def solution(
    map: List[List[str]], instructions: List[Union[str, int]], verbose: bool = False
) -> int:

    # Initialize dimenions
    n_rows = len(map)
    n_cols = len(map[0])

    # Initialize mapper to get the new direction
    new_direction = {
        "r": {
            "L": "u",  # if we look right, turn counter-clockwise, we look up (u)
            "R": "d",  # if we look right, turn clockwise, we look down (d)
        },
        "d": {
            "L": "r",  # if we look down, turn counter-clockwise, we look right (r)
            "R": "l",  # if we look down, turn clockwise, we look left (l)
        },
        "l": {
            "L": "d",  # if we look left, turn counter-clockwise, we look down (d)
            "R": "u",  # if we look left, turn clockwise, we look up ()
        },
        "u": {
            "L": "l",  # if we look up, turn counter-clockwise, we look left (l)
            "R": "r",  # if we look up, turn clockwise, we look right (r)
        },
    }

    # Initialize mapper to change x position depending on the direction
    new_x_delta = {"u": 0, "d": 0, "r": 1, "l": -1}

    # Initialize mapper to change y position depending on the direction
    new_y_delta = {"u": -1, "d": 1, "r": 0, "l": 0}

    # Get an auxilary dictionary that gives us the leftmost and rightmost x positions
    new_x_wrapping = dict()
    for i in range(1, n_rows - 1):
        non_space_idx = [j for j in range(1, n_cols - 1) if map[i][j] != " "]
        new_x_wrapping[i] = {"r": non_space_idx[0], "l": non_space_idx[-1]}

    # Get an auxilary dictionary that gives us the topmost and bottommost y positions
    new_y_wrapping = dict()
    for j in range(1, n_cols - 1):
        non_space_idx = [i for i in range(1, n_rows - 1) if map[i][j] != " "]
        new_y_wrapping[j] = {"d": non_space_idx[0], "u": non_space_idx[-1]}

    # Initialize the x- and y-indices and direction at the beginning
    y = 1
    x = new_x_wrapping[1]["r"]  # first non-space element
    d = "r"

    # Traverse the map as specified by the instructions
    for inst in instructions:
        # Update the direction if needed
        if inst in ["L", "R"]:
            d = new_direction[d][inst]
        # Update the position if needed
        else:
            # Make as many steps as specified
            if verbose:
                print("\nMoving {} for {} steps:".format(d, inst))
            for _ in range(inst):

                # Get new candidate position
                x_cand = x + new_x_delta[d]
                y_cand = y + new_y_delta[d]

                # Check if we need to wrap around
                if map[y_cand][x_cand] == " ":
                    if d in ["r", "l"]:
                        x_cand = new_x_wrapping[y][d]
                    elif d in ["u", "d"]:
                        y_cand = new_y_wrapping[x][d]

                # Move only if the new position is not blocked with an "#"
                if map[y_cand][x_cand] != "#":
                    y = y_cand
                    x = x_cand

                if verbose:
                    print("y: {}, x: {}".format(y, x))

    # Compute and return result
    d_constant = {"r": 0, "d": 1, "l": 2, "u": 3}
    result = 1000 * y + 4 * x + d_constant[d]
    return result


if __name__ == "__main__":

    filepath = pathlib.Path("22/input.txt")
    map = get_map(filepath)
    instructions = get_instructions(filepath)
    print(solution(map, instructions))  # correct: 76332

    # Test 1
    filepath = pathlib.Path("22/input_test_1.txt")
    map = get_map(filepath)
    instructions = get_instructions(filepath)
    expected = 6032
    assert solution(map, instructions) == expected
