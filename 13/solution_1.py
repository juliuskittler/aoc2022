"""2022, day 13, part 1: https://adventofcode.com/2022/day/13."""
import pathlib

from utils import get_lists, lists_are_in_order


def solution(filepath: pathlib.Path) -> int:

    lists = get_lists(filepath)

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

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 5198

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 13
    assert solution(filepath) == expected

    # Test 2
    filepath = dirpath / "input_test_2.txt"
    expected = 0
    assert solution(filepath) == expected
