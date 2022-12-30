"""2022, day 20, part 1: https://adventofcode.com/2022/day/20.

- The positions are not exactly aligned with the example from the problem statement but
that is no issue since the correct order is preserved. Example: If there is a -2 at
index 2, the new position will be inserted at 2-2=0. I.e. it will be insertet at the
beginning of the list, whereas in the example it's inserted at the end of the list.
That's no issue because however, because if we inserted at the beginning of the list at
position 0, we shift the current value at position 0 to position 1. This means that
the inserted element is left to the current element at position 0 in any case.
- The input sequence can contain duplicate values. The example input does not but the
actual input does. Therefore, we make use of a list of tuples (i_old, val) so that
each element is uniquely idenfied.
- Descriptions:
    - i_old is the index of the value in the original input sequence.
    - i_now is the index of the value at the beginning of the current iteration.
    - i_new is the index of the value at the end of the current iteration.
"""


import pathlib
from typing import Tuple


def solution(sequence: Tuple[int]) -> int:

    sequence_len = len(sequence)
    sequence_old = [(i_old, val) for i_old, val in enumerate(sequence)]
    sequence_new = [(i_old, val) for i_old, val in enumerate(sequence)]

    # Iterate through each element in the input sequence
    for (i_old, val) in sequence_old:

        # Get index of current element after the shifts from the previous iterations
        i_now = sequence_new.index((i_old, val))

        # Compute the new index of the current element
        i_new = (i_now + val) % (sequence_len - 1)

        # Change the position
        sequence_new.pop(i_now)  # remove element in current position
        sequence_new.insert(i_new, (i_old, val))  # add element in new position

    # Compute the result:
    sum_of_keys = 0
    i_start = [val for _, val in sequence_new].index(0)
    for delta in [1000, 2000, 3000]:
        i_key = (i_start + delta) % sequence_len
        i_old, delta = sequence_new[i_key]
        sum_of_keys += delta

    return sum_of_keys


if __name__ == "__main__":

    filepath = pathlib.Path("20/input.txt")
    with open(filepath, "r") as f:
        sequence = tuple(map(int, f.read().splitlines()))

    print(solution(sequence))  # correct: 4151

    # Test 1
    filepath = pathlib.Path("20/input_test_1.txt")
    with open(filepath, "r") as f:
        sequence_test = tuple(map(int, f.read().splitlines()))
    expected = 3
    assert solution(sequence_test) == expected
