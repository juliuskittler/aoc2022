"""2022, day 3, part 1: https://adventofcode.com/2022/day/3."""
import pathlib
import string


def solution(filepath: pathlib.Path) -> int:

    with open(filepath, "r") as f:
        rucksack_contents = f.read().splitlines()

    # Initialize useful variables
    priority_sum = 0
    priority_dict_lower = {key: i + 1 for i, key in enumerate(string.ascii_lowercase)}
    priority_dict_upper = {key: i + 27 for i, key in enumerate(string.ascii_uppercase)}
    priority_dict = {**priority_dict_lower, **priority_dict_upper}

    # Loop through all rucksacks and for each of them identify the priority
    # of the item that is in both compartments and sum up this priority
    for content in rucksack_contents:
        # Split content of current rucksack into 2 compartments
        n = len(content)
        content_a = content[0 : n // 2]
        content_b = content[n // 2 :]

        # Identify which element appears in both compartments
        for item_a in content_a:
            if item_a in content_b:
                item_dup = item_a

        # Add its value to our counter
        priority_sum += priority_dict[item_dup]

    return priority_sum


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 8039

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 157
    assert solution(filepath) == expected
