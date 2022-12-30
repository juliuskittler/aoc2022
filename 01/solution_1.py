"""2022, day 1, part 1."""
import pathlib
from typing import List


def solution(inventory_list: List[str]) -> int:

    # Initialize useful variables
    max_calories_per_elf = 0
    calories_of_current_elf = 0

    # Iterate over each item in the inventory, summing up calories for each elf
    for i, item in enumerate(inventory_list):
        if len(item) > 0:
            calories_of_current_elf += int(item)
        elif len(item) == 0:
            max_calories_per_elf = max(max_calories_per_elf, calories_of_current_elf)
            calories_of_current_elf = 0

    # Check if the last elf has more inventory than the others
    max_calories_per_elf = max(max_calories_per_elf, calories_of_current_elf)
    calories_of_current_elf = 0

    return max_calories_per_elf


if __name__ == "__main__":

    # Input data
    filepath = pathlib.Path("01/input.txt")
    with open(filepath, "r") as f:
        inventory_list = f.read().splitlines()

    # Result
    print(solution(inventory_list))  # correct: 67622

    # Test 1
    inventory_list_test = ["1", "2", "", "300"]
    expected = 300
    assert solution(inventory_list_test) == expected

    # Test 2
    inventory_list_test = ["1", "2", ""]
    expected = 3
    assert solution(inventory_list_test) == expected
