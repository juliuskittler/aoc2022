"""2022, day 20, part 2: https://adventofcode.com/2022/day/20."""
import pathlib


def solution(filepath: pathlib.Path) -> int:

    with open(filepath, "r") as f:
        sequence = tuple(map(int, f.read().splitlines()))

    # Initialize useful variables
    sequence_len = len(sequence)
    sequence_old = [(i_old, val * 811589153) for i_old, val in enumerate(sequence)]
    sequence_new = [(i_old, val * 811589153) for i_old, val in enumerate(sequence)]

    # This time, we conduct 10 iterations
    for iter in range(10):

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

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 7848878698663

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 1623178306
    assert solution(filepath) == expected
