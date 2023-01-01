"""2022, day 4, part 2: https://adventofcode.com/2022/day/4."""
import pathlib
import re


def solution(filepath: pathlib.Path) -> int:

    # https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
    with open(filepath, "r") as f:
        assignment_pairs = f.read().splitlines()
        assignment_pairs = [
            list(map(int, re.split("-|,", item))) for item in assignment_pairs
        ]

    # Initialize useful variables
    number_of_pairs_with_partial_overlap = 0

    # Loop through all assignment pairs and count the number of
    # cases where one assignment is overlaps with the other
    for pair in assignment_pairs:
        start_a, end_a, start_b, end_b = pair
        a_before_b = end_a < start_b
        b_before_a = end_b < start_a
        if (not a_before_b) and (not b_before_a):
            number_of_pairs_with_partial_overlap += 1

    return number_of_pairs_with_partial_overlap


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 888

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 4
    assert solution(filepath) == expected
