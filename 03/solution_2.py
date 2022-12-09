"""2022, Day 3, Part 2"""
import pathlib
import string
from typing import List


def solution(rucksack_contents: List[str]) -> int:
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

    # Input data
    filepath = pathlib.Path("03/input.txt")
    with open(filepath, "r") as f:
        rucksack_contents = f.read().splitlines()

    # Result
    print(solution(rucksack_contents))  # correct: 2510

    # Test 1
    rucksack_contents_test = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    expected = 70
    assert solution(rucksack_contents_test) == expected

    # Test 2
    rucksack_contents_test = [
        "aa",
        "aa",
        "aa",
    ]
    expected = 1
    assert solution(rucksack_contents_test) == expected

    # Test 3
    rucksack_contents_test = [
        "aa",
        "aa",
        "aa",
        "AA",
        "AA",
        "AA",
    ]
    expected = 1 + 27  # 27+1
    assert solution(rucksack_contents_test) == expected
