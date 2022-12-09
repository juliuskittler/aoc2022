"""2022, Day 3, Part 1"""
import pathlib
import string
from typing import List


def solution(rucksack_contents: List[str]) -> int:
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

    # Input data
    filepath = pathlib.Path("03/input.txt")
    with open(filepath, "r") as f:
        rucksack_contents = f.read().splitlines()

    # Result
    print(solution(rucksack_contents))  # correct: 8039

    # Test 1
    rucksack_contents_test = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    expected = 157
    assert solution(rucksack_contents_test) == expected

    # Test 2
    rucksack_contents_test = [
        "aa",
        "bb",
        "cc",
        "dd",
    ]
    expected = 10  # 1+2+3+4
    assert solution(rucksack_contents_test) == expected

    # Test 3
    rucksack_contents_test = [
        "AA",
        "BB",
        "CC",
        "DD",
    ]
    expected = 114  # 27+28+29+30
    assert solution(rucksack_contents_test) == expected
