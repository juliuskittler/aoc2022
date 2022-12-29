import pathlib
import re
from typing import Dict


def get_action_dict(filepath: pathlib.Path) -> Dict:
    """Auxilary function to read and parse what the monkey's say."""
    # Initialize output dictionary
    action_dict = {}

    # For each monkey from the file, we add its information to the output dictionary
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

        for line in lines:

            # Extract monkey name
            monkey = line.split(":")[0]

            # Extract number if it exists
            numbers = list(re.findall("[0-9]+", line))
            if len(numbers) > 0:
                number = int(numbers[0])
            else:
                number = None

            # Extract computation if it exists
            if number is None:
                line_split = line.split(" ")
                mky_l = line_split[1]
                operator = line_split[2]
                mky_r = line_split[3]
            else:
                mky_l = None
                operator = None
                mky_r = None

            # Add everything to the dict
            action_dict[monkey] = {
                "num": number,
                "mky_l": mky_l,
                "operator": operator,
                "mky_r": mky_r,
            }

    return action_dict
