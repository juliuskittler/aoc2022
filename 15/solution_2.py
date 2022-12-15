import pathlib
from typing import List, Tuple

from utils import get_coords, manhattan_distance

"""
Note:
- We need to find the 1 position that is not covered by the range of any sensors.
- For this purpose, we need to essentially check all positions between x and y 
coordinates of 0 to 4000000. 
- The implementation from solution_1.py is way to inefficient for this.
"""


def solution(
    sensor_coords: List[Tuple],
    beacon_coords: List[Tuple],
    max_coord: int,
    min_coord: int = 0,
) -> int:

    # Initialize useful variables
    n_pairs = len(sensor_coords)
    available_x_idx = {i for i in range(min_coord, max_coord + 1)}

    # Compute manhattan distances for each sensor and affected ranges of rows
    dist_dict = {}
    rows_dict = {}
    for i in range(n_pairs):
        dist = manhattan_distance(sensor_coords[i], beacon_coords[i])
        dist_dict[sensor_coords[i]] = dist

        min_row = sensor_coords[i][1] - dist
        max_row = sensor_coords[i][1] + dist
        rows_dict[sensor_coords[i]] = (min_row, max_row)

    # Iterate over each row in scope
    for row_idx in range(min_coord, max_coord + 1):
        if row_idx % 10 == 0:
            print(row_idx)

        positions_reached_on_row_idx = set()

        # Iterate over each sensor
        for i in range(n_pairs):

            # Check if the current sensor matters for the current row_idx
            min_row, max_row = rows_dict[sensor_coords[i]]

            if row_idx >= min_row and row_idx <= max_row:

                # Retrieve manhattan distance
                dist = dist_dict[sensor_coords[i]]

                # Check quickly if the current sensor reaches the row of interest
                distance_to_row_idx = abs(sensor_coords[i][1] - row_idx)

                # If necessary, compute the positions reached by the sensor
                start_x_idx = sensor_coords[i][0] - (dist - distance_to_row_idx)
                end_x_idx = sensor_coords[i][0] + (dist - distance_to_row_idx) + 1
                positions_reached_on_row_idx = positions_reached_on_row_idx.union(
                    set(range(start_x_idx, end_x_idx))
                )

        # Check if there is any position that is not covered and if so, stop...
        not_covered = available_x_idx - positions_reached_on_row_idx
        if len(not_covered) > 0:
            distress_x_idx = [coords for coords in not_covered][0]
            distress_y_idx = row_idx
            tuning_frequency = distress_x_idx * 4000000 + distress_y_idx
            return tuning_frequency


if __name__ == "__main__":

    filepath = pathlib.Path("15/input.txt")
    sensor_coords, beacon_coords = get_coords(filepath)
    max_coord = 4000000

    print(solution(sensor_coords, beacon_coords, max_coord))  # correct:

    # Test 1
    filepath = pathlib.Path("15/input_test_1.txt")
    sensor_coords_test, beacon_coords_test = get_coords(filepath)
    max_coord = 20
    expected = 56000011
    print(solution(sensor_coords_test, beacon_coords_test, max_coord))
    assert (solution(sensor_coords_test, beacon_coords_test, max_coord)) == expected
