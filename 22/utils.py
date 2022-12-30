import pathlib
from typing import List, Union


def get_instructions(filepath: pathlib.Path) -> List[Union[str, int]]:
    """Auxilary function to get the instructions."""
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

        # Extract line with instructions. Last line holds the instructions
        instructions = lines[-1]

        # Add a space after every R and L so we can split on it
        instructions = "".join(
            [
                " " + val + " " if val == "R" or val == "L" else val
                for val in instructions
            ]
        )
        instructions = [
            val if val == "R" or val == "L" else int(val)
            for val in instructions.split()
        ]

        return instructions


def get_map(filepath: pathlib.Path) -> List[Union[str, int]]:
    """Auxilary function to get the map."""
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

        # Extract the lines with the map. All lines except the last 2 hold our map.
        map = lines[0:-2]

        # We add spaces around the map (for convenience later on)
        max_rowlen = 0
        for i in range(len(map)):
            map[i] = " " + map[i] + " "
            rowlen = len(map[i])
            if rowlen > max_rowlen:
                max_rowlen = rowlen
        for i in range(len(map)):
            rowlen = len(map[i])
            spaces_to_add = max_rowlen - rowlen
            if spaces_to_add > 0:
                map[i] = map[i] + "".join([" " for _ in range(spaces_to_add)])

        map.insert(0, "".join([" " for _ in range(max_rowlen)]))
        map.append("".join([" " for _ in range(max_rowlen)]))

        return map
