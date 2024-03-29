"""2022, day 15, part 1: https://adventofcode.com/2022/day/15.

Importantly, the input coordinates have coordinates that lie very far from each other
(e.g. 87472 vs. 3045894). Therefore, we want to avoid constructing a map that covers all
 coordinates. Instead, we want to focus on the row that we are interested in.
- For each sensor S,
    - ... compute the manhattan distance D to its closest beacon.
    - ... check if the same manhattan distance D reaches the given row R at any
    position (by checking directly above or below the sensor position,
    i.e. on the same x-axis coordinate).
        - If it does, compute all positions on the given row R that are reached by
        the sensor S with the manhattan distance D.
        - Put these positions into a set.
- Return the length of the set.
"""

import pathlib

from utils import get_coords, manhattan_distance


def solution(filepath: pathlib.Path, row_idx: int) -> int:

    sensor_coords, beacon_coords = get_coords(filepath)

    # Initialize useful variables
    positions_reached_on_row_idx = set()
    n_pairs = len(sensor_coords)

    # Iterate over each sensor
    for i in range(n_pairs):

        # Compute manhattan distance between sensor and beacon
        dist = manhattan_distance(sensor_coords[i], beacon_coords[i])

        # Check quickly if the current sensor reaches the row of interest
        distance_to_row_idx = abs(sensor_coords[i][1] - row_idx)
        sensor_reaches_row_idx = distance_to_row_idx <= dist

        # If necessary, compute the positions reached by the sensor
        if sensor_reaches_row_idx:
            start_x_idx = sensor_coords[i][0] - (dist - distance_to_row_idx)
            end_x_idx = sensor_coords[i][0] + (dist - distance_to_row_idx) + 1
            for x_idx in range(start_x_idx, end_x_idx):
                positions_reached_on_row_idx.add(x_idx)

    # Remove all positions where a beacon is already present
    for i in range(n_pairs):
        if beacon_coords[i][1] == row_idx:
            positions_reached_on_row_idx -= {beacon_coords[i][0]}

    # Return the number of positions reached by the sensors on row_idx
    n_positions_reached = len(positions_reached_on_row_idx)
    return n_positions_reached


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    row_idx = 2000000
    print(solution(filepath, row_idx))  # correct: 4985193

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    row_idx = 10
    expected = 26
    assert (solution(filepath, row_idx)) == expected

    # Test 2
    filepath = dirpath / "input_test_2.txt"
    sensor_coords_test, beacon_coords_test = get_coords(filepath)
    row_idx = 10
    expected = 12
    assert (solution(filepath, row_idx)) == expected

    # Test 3
    filepath = dirpath / "input_test_3.txt"
    sensor_coords_test, beacon_coords_test = get_coords(filepath)
    row_idx = 10
    expected = 16
    assert (solution(filepath, row_idx)) == expected
