"""2022, day 15, part 2.

- We need to find the 1 position that is not covered by the range of any sensors.
- For this purpose, we need to essentially check all positions between x and y
coordinates of 0 to 4000000. The implementation from solution_1.py is too inefficient!
- I'm using this hint. It illustrates that we don't need to iterate over all coordinates:
https://www.reddit.com/r/adventofcode/comments/zmfwg1/2022_day_15_part_2_seekin_for_the_beacon/
- Approach:
    - We need to iterate over the coordinates of 1 position outside of the outer
limit of each sensor and add them to a dictionary as a key (only if they fall within
the range of our min. and max. coordinates of x and y).
    - As value of the corresponding
key, we keep track of the count of the respective coordinate. Since the range of each
sensor is diamond shaped but the range of the grid is diagonal shaped we know the
following about the position of the distress signal:
        - If the position is not on the edges or corners of the grid, it will be located
        between at least 4 different diamonds, i.e. between the range of at least
        4 different sensors:
        ###
        # #
        ###
        - If the position is on the edges of the grid (not on the corners), it will be
        located between at least 2 different diamonds, i.e. between the range of at
        least 2 different sensors:
        ###      # #      ###      ###
         ##  or  ###  or  ##   or  ###
        ###      ###      ###      # #
        - If the position is in one of the 4 corners of the grid, it will be located
        at the outer range of at least 1 different diamond
         ##      ##       ###      ###
        ###  or  ###  or  ###  or  ###
        ###      ###      ##        ##
    - Basically, we have the following process:
        - We sort positions that are located at the edge of a diamond by the number of
        times they appear at the edge of a diamond descendingly.
        - Then, for each position, we check if it is reachable by any sensor. If not,
        this position is used for the solution.
- My implementation is still slow... but hey it works :)
"""


import pathlib
from typing import List, Tuple

from utils import get_coords, manhattan_distance


def solution(
    sensor_coords: List[Tuple],
    beacon_coords: List[Tuple],
    max_coord: int,
    min_coord: int = 0,
) -> int:

    n_sensors = len(sensor_coords)

    # How many times was a particular coordinate just 1 step outside the range of any
    # sensor? We keep track of this count only for the required coordinates.
    limit_coords_cnt = dict()

    # Compute manhattan distances for each sensor
    dist_dict = {}
    for i in range(n_sensors):
        dist = manhattan_distance(sensor_coords[i], beacon_coords[i])
        dist_dict[sensor_coords[i]] = dist

    # Iterate over each sensor
    for i in range(n_sensors):

        # Compute manhattan distances
        dist = manhattan_distance(sensor_coords[i], beacon_coords[i])

        # Prepare useful variables
        dist += 1
        delta_y = -dist
        delta_x = 0

        # We start at the top, then move right down, left down, left up, right up
        next_position = (sensor_coords[i][0] + delta_x, sensor_coords[i][1] + delta_x)
        if next_position not in limit_coords_cnt:
            limit_coords_cnt[next_position] = 1
        else:
            limit_coords_cnt[next_position] = limit_coords_cnt[next_position] + 1

        # Get next position
        delta_y += 1
        delta_x += 1
        next_position = (sensor_coords[i][0] + delta_x, sensor_coords[i][1] + delta_x)

        # Iterate over the coordinates just 1 step outside the range of the sensor
        while delta_y != -dist:  # loop until we reach start position

            # Update our limit coordinate count for the current position
            in_valid_range = (
                next_position[0] <= max_coord
                and next_position[0] >= min_coord
                and next_position[1] <= max_coord
                and next_position[1] >= min_coord
            )

            if in_valid_range:
                if next_position not in limit_coords_cnt:
                    limit_coords_cnt[next_position] = 1
                else:
                    limit_coords_cnt[next_position] = (
                        limit_coords_cnt[next_position] + 1
                    )

            # Update the next position
            if delta_y == -dist or (delta_x > 0 and delta_y < 0):  # move right down
                delta_y += 1
                delta_x += 1
            elif delta_x == dist or (delta_x > 0 and delta_y > 0):  # move left down
                delta_y += 1
                delta_x -= 1
            elif delta_y == dist or (delta_x < 0 and delta_y > 0):  # move right up
                delta_y -= 1
                delta_x -= 1
            elif delta_x == -dist or (delta_x < 0 and delta_y < 0):  # move left up
                delta_y -= 1
                delta_x += 1
            next_position = (
                sensor_coords[i][0] + delta_x,
                sensor_coords[i][1] + delta_y,
            )

    # Sort the positions by count
    sorted_positions = reversed(
        sorted(zip(limit_coords_cnt.values(), limit_coords_cnt.keys()))
    )
    sorted_positions = [position for _, position in sorted_positions]

    # For each position, check if it is reachable by any sensors.
    for position in sorted_positions:

        is_reachable = False

        for i in range(n_sensors):

            # Compute manhattan distance between sensor and current position
            dist = manhattan_distance(sensor_coords[i], position)

            # Check if the point is reachable by the sensor, i.e. if it falls within
            # the range of the manhattan distance from closest beakon to the sensor.
            is_reachable = dist <= dist_dict[sensor_coords[i]]
            if is_reachable:
                break  # Skip other sensors if position is reachable by any sensor

        # If it's not reachable, use this position for our answer.
        if not is_reachable:
            distress_x_idx, distress_y_idx = position
            break

    # Return tuning frequency
    tuning_frequency = distress_x_idx * 4000000 + distress_y_idx
    return tuning_frequency


if __name__ == "__main__":

    filepath = pathlib.Path("15/input.txt")
    sensor_coords, beacon_coords = get_coords(filepath)
    max_coord = 4000000

    print(solution(sensor_coords, beacon_coords, max_coord))  # correct: 11583882601918

    # Test 1
    filepath = pathlib.Path("15/input_test_1.txt")
    sensor_coords_test, beacon_coords_test = get_coords(filepath)
    max_coord = 20
    expected = 56000011
    assert (solution(sensor_coords_test, beacon_coords_test, max_coord)) == expected
