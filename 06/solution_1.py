"""2022, day 6, part 1: https://adventofcode.com/2022/day/6."""
import pathlib


def solution(filepath: pathlib.Path, marker_len: int = 4) -> int:
    """Return first index of first sequence with marker_len different characters."""
    with open(filepath, "r") as f:
        datastream = f.read()

    n = len(datastream)

    # Loop through the string, keeping a window of 'marker_len' characters and check
    # if these 'marker_len' characters are unique for each of them.
    for i in range(0, n - marker_len + 1):
        candidate = datastream[i : (i + marker_len)]
        n_unique_characters = len(set(candidate))
        if n_unique_characters == marker_len:
            return i + marker_len
    return None


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 1757

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 7
    assert solution(filepath) == expected

    # Test 2
    filepath = dirpath / "input_test_2.txt"
    expected = 5
    assert solution(filepath) == expected

    # Test 3
    filepath = dirpath / "input_test_3.txt"
    expected = 6
    assert solution(filepath) == expected

    # Test 4
    filepath = dirpath / "input_test_4.txt"
    expected = 10
    assert solution(filepath) == expected

    # Test 5
    filepath = dirpath / "input_test_5.txt"
    expected = 11
    assert solution(filepath) == expected
