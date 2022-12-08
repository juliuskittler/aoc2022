"""2022, Day 5, Part 2"""
import pathlib
import re
from typing import List, Tuple


def solution(instructions: List[Tuple], stacks: List[List]) -> int:
    # Iterate over instructions and adjust the stacks accordingly
    for instruction in instructions:
        how_many, from_stack, to_stack = instruction

        # Update the to-stack (as we are adding elements)
        stacks[to_stack - 1].extend(stacks[from_stack - 1][(-how_many):])

        # Update the from-stack (as we are removing elements)
        stacks[from_stack - 1] = stacks[from_stack - 1][:(-how_many)]
        # print(stacks)

    # Get the top crates of each stack as a string
    crates_on_top = "".join([stack[-1] if len(stack) > 0 else "" for stack in stacks])
    return crates_on_top


if __name__ == "__main__":

    # Input data
    filepath = pathlib.Path("05/input.txt")
    with open(filepath, "r") as f:
        my_input = f.read()  # .splitlines()

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
        row_indices = list(range(0, len(stacks_str) - 1))
        stacks = []
        for col in col_indices:
            new_stack = []
            for row in range(0, len(stacks_str) - 1):
                value = stacks_str[row][col[0] : col[1]]
                if value != " ":
                    new_stack.append(value)
            stacks.append(list(reversed(new_stack)))

    # Result
    print(solution(instructions, stacks))  # correct: CQQBBJFCS

    # Test 1
    instructions_test = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]
    stacks_test = [["Z", "N"], ["M", "C", "D"], ["P"]]
    expected = "MCD"
    assert solution(instructions_test, stacks_test) == expected
