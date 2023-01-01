"""2022, day 4, part 1: https://adventofcode.com/2022/day/4."""
import pathlib
import re
from typing import List


def solution(filepath: pathlib.Path) -> int:

    # https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
    with open(filepath, "r") as f:
        assignment_pairs = f.read().splitlines()
        assignment_pairs = [
            list(map(int, re.split("-|,", item))) for item in assignment_pairs
        ]

    # Initialize useful variables
    number_of_pairs_with_full_overlap = 0

    # Loop through all assignment pairs and count the number of
    # cases where one assignment is fully contained in the other
    for pair in assignment_pairs:
        start_a, end_a, start_b, end_b = pair
        a_in_b = (start_a >= start_b) and (end_a <= end_b)
        b_in_a = (start_b >= start_a) and (end_b <= end_a)
        if a_in_b or b_in_a:
            number_of_pairs_with_full_overlap += 1

    return number_of_pairs_with_full_overlap


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 471

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 2
    assert solution(filepath) == expected
