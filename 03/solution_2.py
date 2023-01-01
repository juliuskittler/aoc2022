"""2022, day 3, part 2: https://adventofcode.com/2022/day/3."""
import pathlib
import string


def solution(filepath: pathlib.Path) -> int:

    with open(filepath, "r") as f:
        rucksack_contents = f.read().splitlines()

    # Check inputs
    n = len(rucksack_contents)
    assert n % 3 == 0, "Number of rucksack contents is perfectly divisible by 3."

    # Initialize useful variables
    priority_sum = 0
    priority_dict_lower = {key: i + 1 for i, key in enumerate(string.ascii_lowercase)}
    priority_dict_upper = {key: i + 27 for i, key in enumerate(string.ascii_uppercase)}
    priority_dict = {**priority_dict_lower, **priority_dict_upper}

    # Loop through groups of 3 rucksack_contents each
    start_group_idx = 0
    while start_group_idx < n:
        # Retrieve the 3 rucksack_contents of the current group
        content_a = rucksack_contents[start_group_idx]
        content_b = rucksack_contents[start_group_idx + 1]
        content_c = rucksack_contents[start_group_idx + 2]

        # Identify which element appears in all 3 compartments
        for item_a in content_a:
            if item_a in content_b and item_a in content_c:
                item_dup = item_a

        # Add its value to our counter
        priority_sum += priority_dict[item_dup]

        # Increase counter
        start_group_idx += 3

    return priority_sum


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 2510

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 70
    assert solution(filepath) == expected
