"""2022, day 5, part 1: https://adventofcode.com/2022/day/5."""
import pathlib

from utils import parse_input


def solution(filepath: pathlib.Path) -> int:

    stacks, instructions = parse_input(filepath)

    # Iterate over instructions and adjust the stacks accordingly
    for instruction in instructions:
        how_many, from_stack, to_stack = instruction
        for i in range(how_many):
            crate = stacks[from_stack - 1].pop()
            stacks[to_stack - 1].append(crate)

    # Get the top crates of each stack as a string
    crates_on_top = "".join([stack[-1] if len(stack) > 0 else "" for stack in stacks])
    return crates_on_top


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: RFFFWBPNS

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = "CMZ"
    assert solution(filepath) == expected
