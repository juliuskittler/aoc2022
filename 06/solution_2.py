"""2022, day 6, part 2: https://adventofcode.com/2022/day/6."""
import pathlib


def solution(datastream: str, marker_len: int = 14) -> int:
    """Return first index of first sequence with marker_len different characters."""
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

    filepath = pathlib.Path("06/input.txt")
    with open(filepath, "r") as f:
        datastream = f.read()

    # Result
    print(solution(datastream))  # correct: 2950

    # Test 1
    datastream_test = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    expected = 19
    assert solution(datastream_test) == expected

    # Test 2
    datastream_test = "bvwbjplbgvbhsrlpgdmjqwftvncz"
    expected = 23
    assert solution(datastream_test) == expected

    # Test 3
    datastream_test = "nppdvjthqldpwncqszvftbrmjlhg"
    expected = 23
    assert solution(datastream_test) == expected

    # Test 4
    datastream_test = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
    expected = 29
    assert solution(datastream_test) == expected

    # Test 5
    datastream_test = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    expected = 26
    assert solution(datastream_test) == expected
