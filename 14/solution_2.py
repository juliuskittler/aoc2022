import copy
import pathlib
from typing import List

from utils import get_new_position, get_rock_paths


def solution(rock_paths: List[List[List[int]]]):

    rock_paths = copy.deepcopy(rock_paths)

    # Initialize position from where the sand falls
    hole_x = 500
    hole_y = 0

    # Identify the min and max indices from the rock paths
    max_x = -1
    max_y = -1
    min_x = int(9e10)

    for path in rock_paths:
        for position in path:
            if position[0] < min_x:
                min_x = position[0]
            if position[0] > max_x:
                max_x = position[0]
            if position[1] > max_y:
                max_y = position[1]

    # Ensure that there is enough space on the x-axis for sandcorns to fall diagonally
    # We do this by adding 2x max_y to our max_x.
    max_x += 2 * max_y

    # Update all indices based on min and max indices to save space in our rock map
    hole_x = hole_x - min_x + max_y
    hole_idx = (hole_x, hole_y)

    for path in rock_paths:
        for position in path:
            position[0] = position[0] - min_x + max_y

    max_x = max_x - min_x + 1
    min_x = 0

    # Initialize a rock map
    rock_map = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    rock_map[hole_y][hole_x] = "+"

    # Iterate over each path in order to add the stone paths to the rock map
    for path in rock_paths:

        # Iterate over each pair of subsequent positions in the current path
        for i in range(0, len(path) - 1):
            pos_start = path[i]
            pos_end = path[i + 1]

            # Check if the positions have the same x-axis or the same y-axis values.
            # If the x-axis is the same, iterate across the y-axis and vice versa,
            # adding '#' to the rock_map until we reach from the start position to
            # the end position.
            if pos_start[1] == pos_end[1]:  # change x
                if pos_end[0] > pos_start[0]:
                    step = 1
                else:
                    step = -1
                for x_idx in range(pos_start[0], pos_end[0], step):
                    rock_map[pos_start[1]][x_idx] = "#"
            elif pos_start[0] == pos_end[0]:  # change y
                if pos_end[1] > pos_start[1]:
                    step = 1
                else:
                    step = -1
                for y_idx in range(pos_start[1], pos_end[1], step):
                    rock_map[y_idx][pos_start[0]] = "#"

        # Fill last position
        rock_map[pos_end[1]][pos_end[0]] = "#"

    # Append to the rock_map one full row of "." and another full row of "#"
    # Update y_max accordingly
    row_of_dots = ["." for _ in range(len(rock_map[0]))]
    row_of_hashtags = ["#" for _ in range(len(rock_map[0]))]
    rock_map.append(row_of_dots)
    rock_map.append(row_of_hashtags)

    # Now we fill the rock_map with sand until it's not possible anymore
    sand_cnt = 0
    cave_full = False
    x_prev, y_prev = hole_idx
    while not cave_full:

        # Initialize positions of new sand corn
        x, y = hole_idx

        # Fall down vertically as far as possible
        keep_moving, x, y = get_new_position(x, y, rock_map)
        while keep_moving:
            keep_moving, x, y = get_new_position(x, y, rock_map)

        # If we can add the sand corn, add it to the rock_map
        cave_full = (x_prev == x) and (y_prev == y)
        if not cave_full:
            rock_map[y][x] = "o"
            sand_cnt += 1

        # Keep track of position of last added sandcorn
        x_prev = x
        y_prev = y

    return sand_cnt


if __name__ == "__main__":

    filepath = pathlib.Path("14/input.txt")
    rock_paths = get_rock_paths(filepath)

    print(solution(rock_paths))  # correct: 25248

    # Test 1
    filepath = pathlib.Path("14/input_test_1.txt")
    rock_paths_test = get_rock_paths(filepath)
    expected = 93
    assert solution(rock_paths_test) == expected
