import pathlib
import re
from typing import List, Tuple


def get_coords(filepath: pathlib.Path) -> Tuple[List[Tuple]]:
    """Returns a tuple of two lists.

    The first list contains tuples with the coordinates of the sensors.
    The second list contains tuples with the coordinates of the corresponding beacons.
    """

    with open(filepath, "r") as f:
        lines = f.read().splitlines()
        sensor_coords = list()
        beacon_coords = list()
        for line in lines:
            sensor_coord = (
                int(re.findall("x=(-?\d+)", line)[0]),
                int(re.findall("y=(-?\d+)", line)[0]),
            )
            sensor_coords.append(sensor_coord)
            beacon_coord = (
                int(re.findall("x=(-?\d+)", line)[1]),
                int(re.findall("y=(-?\d+)", line)[1]),
            )
            beacon_coords.append(beacon_coord)

    return (sensor_coords, beacon_coords)


def manhattan_distance(coord_a: Tuple, coord_b: Tuple) -> int:
    """Auxilary function to compute the manhattan distnace for 2D Tuples."""
    return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1])
