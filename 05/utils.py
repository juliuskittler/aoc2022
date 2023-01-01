import pathlib
import re
from typing import Tuple


def parse_input(filepath: pathlib.Path) -> Tuple:
    """Auxilary function to parse inputs and return (stacks, instructions)."""
    with open(filepath, "r") as f:
        my_input = f.read()

    # Get instructions in list form
    instructions_str = my_input.split("\n\n")[1].splitlines()
    instructions = [
        tuple(map(int, re.findall("[0-9]+", instr))) for instr in instructions_str
    ]

    # Get stacks in list form
    stacks_str = my_input.split("\n\n")[0].split("\n")
    col_indices = [
        (m.start(0), m.end(0)) for m in re.finditer("[0-9+]", stacks_str[-1])
    ]

    stacks = []
    for col in col_indices:
        new_stack = []
        for row in range(0, len(stacks_str) - 1):
            value = stacks_str[row][col[0] : col[1]]
            if value != " ":
                new_stack.append(value)
        stacks.append(list(reversed(new_stack)))

    return (stacks, instructions)
