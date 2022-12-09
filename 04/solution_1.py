"""2022, Day 4, Part 1"""
import pathlib
import re
from typing import List


def solution(assignment_pairs: List[List[int]]) -> int:
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

    # Input data
    # References:
    # - https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
    # - https://stackoverflow.com/questions/3371269/call-int-function-on-every-list-element
    filepath = pathlib.Path("04/input.txt")
    with open(filepath, "r") as f:
        assignment_pairs = f.read().splitlines()
        assignment_pairs = [
            list(map(int, re.split("-|,", item))) for item in assignment_pairs
        ]

    # Result
    print(solution(assignment_pairs))  # correct: 471

    # Test 1
    assignment_pairs_test = [
        [2, 4, 6, 8],
        [2, 3, 4, 5],
        [5, 7, 7, 9],
        [2, 8, 3, 7],
        [6, 6, 4, 6],
        [2, 6, 4, 8],
    ]
    expected = 2
    assert solution(assignment_pairs_test) == expected

    # Test 2
    assignment_pairs_test = [[2, 4, 6, 8]]
    expected = 0
    assert solution(assignment_pairs_test) == expected

    # Test 3
    assignment_pairs_test = [[2, 3, 2, 5]]
    expected = 1
    assert solution(assignment_pairs_test) == expected

    # Test 4
    assignment_pairs_test = [[1, 3, 2, 5]]
    expected = 0
    assert solution(assignment_pairs_test) == expected