import pathlib
from typing import List, Tuple

from utils import get_coords, manhattan_distance

"""
Note:
- Importantly, the input coordinates have coordinates that lie very far from each other
(e.g. 87472 vs. 3045894). Therefore, we want to avoid constructing a map this time that 
covers all coordinates. Instead, we want to focus on the row that we are interested in.
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


def solution(
    row_idx: int, sensor_coords: List[Tuple], beacon_coords: List[Tuple]
) -> int:

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
    print(sorted([x for x in positions_reached_on_row_idx]))
    # Return the number of positions reached by the sensors on row_idx
    n_positions_reached = len(positions_reached_on_row_idx)
    return n_positions_reached


if __name__ == "__main__":

    filepath = pathlib.Path("15/input.txt")
    sensor_coords, beacon_coords = get_coords(filepath)
    row_idx = 2000000

    print(solution(row_idx, sensor_coords, beacon_coords))  # correct: 4985193

    # Test 1
    filepath = pathlib.Path("15/input_test_1.txt")
    sensor_coords_test, beacon_coords_test = get_coords(filepath)
    row_idx = 10
    expected = 26
    solution(row_idx, sensor_coords_test, beacon_coords_test)
    assert (solution(row_idx, sensor_coords_test, beacon_coords_test)) == expected

    # Test 2
    filepath = pathlib.Path("15/input_test_2.txt")
    sensor_coords_test, beacon_coords_test = get_coords(filepath)
    row_idx = 10
    expected = 12
    assert (solution(row_idx, sensor_coords_test, beacon_coords_test)) == expected

    # Test 3
    filepath = pathlib.Path("15/input_test_3.txt")
    sensor_coords_test, beacon_coords_test = get_coords(filepath)
    row_idx = 10
    expected = 16
    assert (solution(row_idx, sensor_coords_test, beacon_coords_test)) == expected
