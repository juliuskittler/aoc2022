"""2022, day 21, part 1: https://adventofcode.com/2022/day/21.

We start at the root and recursively get the compute the number for each monkey that
does not come with a number and whoose number we need for the root computation.
"""

import pathlib
from typing import Dict

from utils import get_action_dict


def get_number(monkey: str, action_dict: Dict) -> int:
    """Auxilary function go get the number for a particular monkey.

    This function works recursively and returns the number regardless if an operation
    needs to be conducted or if the number for the monkey is directly available.
    """
    if action_dict[monkey]["num"] is not None:
        return action_dict[monkey]["num"]
    else:
        number_mky_l = get_number(action_dict[monkey]["mky_l"], action_dict)
        number_mky_r = get_number(action_dict[monkey]["mky_r"], action_dict)
        operator = action_dict[monkey]["operator"]
        if operator == "+":
            return number_mky_l + number_mky_r
        elif operator == "-":
            return number_mky_l - number_mky_r
        elif operator == "*":
            return number_mky_l * number_mky_r
        elif operator == "/":
            return number_mky_l / number_mky_r


def solution(filepath: pathlib.Path):
    action_dict = get_action_dict(filepath)
    return int(get_number("root", action_dict))


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 110181395003396

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 152
    assert solution(filepath) == expected
