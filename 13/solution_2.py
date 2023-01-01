"""2022, day 13, part 2: https://adventofcode.com/2022/day/13.

- We need to use our lists_are_in_order function to sort all lists in our input!
- Common sorting algorithms are Quicksort, Heapsort Mergesort. We will use Mergesort!
- References:
    - https://en.wikipedia.org/wiki/Sorting_algorithm
    - https://lamfo-unb.github.io/2019/04/21/Sorting-algorithms/#:~:text=%2B1%5D%20%3D%20temp-,Quicksort,greater%20numbers%20on%20the%20right.
"""

import pathlib
from typing import List

from utils import get_lists, merge_sort


def solution(filepath: pathlib.Path) -> int:

    lists = get_lists(filepath)

    # Append the divider packets to our list
    dividers = [[[2]], [[6]]]
    lists.extend(dividers)

    # Sort the lists with merge sort
    merge_sort(lists)

    # Identify indices of divider packets and multiply them
    idx_dividers = list()
    for i, l in enumerate(lists):
        if l in dividers:
            idx_dividers.append(i + 1)
    decoder_key = idx_dividers[0] * idx_dividers[1]
    return decoder_key


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 22344

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 140
    assert solution(filepath) == expected
