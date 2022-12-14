import pathlib
from typing import List, Tuple


def get_rock_paths(filepath: pathlib.Path) -> List[List[List[int]]]:
    """Auxilary function to get the required rock paths."""
    with open(filepath, "r") as f:
        rock_paths = f.read().splitlines()
        rock_paths = [
            [
                [int(position.split(",")[0]), int(position.split(",")[1])]
                for position in path.split(" -> ")
            ]
            for path in rock_paths
        ]
    return rock_paths


def get_new_position(x: int, y: int, rock_map: List[List[int]]) -> Tuple[int]:
    """Auxilary function to compute the next position of a sand corn.

    This function returns a tuple of 3 values:
    (1 if the corn will keep falling and 0 otherwise, new x position, new y position)
    """
    if rock_map[y + 1][x] == ".":
        return (1, x, y + 1)
    elif rock_map[y + 1][x - 1] == ".":
        return (1, x - 1, y + 1)
    elif rock_map[y + 1][x + 1] == ".":
        return (1, x + 1, y + 1)
    else:  # Stay at the position
        return (0, x, y)
