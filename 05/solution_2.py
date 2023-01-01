"""2022, day 5, part 2: https://adventofcode.com/2022/day/5."""
import pathlib

from utils import parse_input


def solution(filepath: pathlib.Path) -> int:

    stacks, instructions = parse_input(filepath)

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

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: CQQBBJFCS

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = "MCD"
    assert solution(filepath) == expected
