"""2022, day 13, part 1: https://adventofcode.com/2022/day/13."""
import pathlib
from typing import List

from utils import get_lists, lists_are_in_order


def solution(lists: List[List]) -> int:

    # Initialize useful variables
    pair_idx_in_order = list()
    n_lists = len(lists)

    # For each list pair, check whether it is in order
    for i in range(0, n_lists, 2):

        list_left = lists[i]
        list_right = lists[i + 1]
        if lists_are_in_order(list_left, list_right):
            pair_idx_in_order.append(i // 2 + 1)

    # Compute the sum of the indices
    sum_of_pair_idx_in_order = sum(pair_idx_in_order)
    return sum_of_pair_idx_in_order


if __name__ == "__main__":

    filepath = pathlib.Path("13/input.txt")
    lists = get_lists(filepath)

    print(solution(lists))  # correct: 5198

    # Test 1
    filepath = pathlib.Path("13/input_test_1.txt")
    lists_test = get_lists(filepath)
    expected = 13
    assert solution(lists_test) == expected

    # Test 2
    filepath = pathlib.Path("13/input_test_2.txt")
    lists_test = get_lists(filepath)
    expected = 0
    assert solution(lists_test) == expected
