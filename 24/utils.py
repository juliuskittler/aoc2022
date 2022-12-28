import pathlib
from typing import Dict, Tuple, Union


def parse_inputs(filepath: pathlib.Path) -> Tuple[Union[Dict, int]]:
    """Returns the tuple (pos_dict, dir_dict, min_i, max_i, min_j, max_j)."""

    with open(filepath, "r") as f:
        lines = f.read().splitlines()

        # Initialize useful variables
        blizzard_idx = 0
        pos_dict = dict()
        dir_dict = dict()

        min_i = 1
        max_i = len(lines) - 2  # minus 2 because we have a wall at top and bottom
        min_j = 1
        max_j = len(lines[0]) - 2  # minus 2 because we have a wall left and right

        # Add each blizzard to our pos_dict and our dir_dict
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):
                if lines[i][j] != "." and lines[i][j] != "#":
                    pos_dict[blizzard_idx] = (i, j)
                    dir_dict[blizzard_idx] = lines[i][j]
                    blizzard_idx += 1

        # Return results
        return (pos_dict, dir_dict, min_i, max_i, min_j, max_j)
