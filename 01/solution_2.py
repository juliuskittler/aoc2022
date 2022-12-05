"""2022, Day 1, Part 2"""
import pathlib
from typing import List


def solution(inventory_list: List, top_k: int = 3) -> int:

    # Initialize useful variables
    calories_of_top_k_elves = [0] * top_k
    calories_of_current_elf = 0

    # Iterate over each item in the inventory, summing up calories for each elf
    for item in inventory_list:

        if len(item) > 0:
            calories_of_current_elf += int(item)
        elif len(item) == 0:
            smallest_calories_of_top_k_elves = min(calories_of_top_k_elves)
            if calories_of_current_elf > smallest_calories_of_top_k_elves:
                idx = calories_of_top_k_elves.index(smallest_calories_of_top_k_elves)
                calories_of_top_k_elves[idx] = calories_of_current_elf
            calories_of_current_elf = 0

    # Check if the last elf should be in the top 3
    smallest_calories_of_top_k_elves = min(calories_of_top_k_elves)
    if calories_of_current_elf > smallest_calories_of_top_k_elves:
        idx = calories_of_top_k_elves.index(smallest_calories_of_top_k_elves)
        calories_of_top_k_elves[idx] = calories_of_current_elf

    # Sum up the calories of the top 3 elves
    total_calories_of_top_k_elves = sum(calories_of_top_k_elves)
    return total_calories_of_top_k_elves


if __name__ == "__main__":

    # Input data
    filepath = pathlib.Path("01/input.txt")
    with open(filepath) as f:
        inventory_list = f.read().splitlines()

    # Result
    print(solution(inventory_list))  # correct: 67622

    # Test 1
    inventory_list_test = ["1", "2", "", "300"]
    expected = 303
    assert solution(inventory_list_test) == expected

    # Test 2
    inventory_list_test = ["1", "2", "", "300", "", "1", "", "5"]
    expected = 308
    assert solution(inventory_list_test) == expected

    # Test 3
    inventory_list_test = ["1", "2", "", "300", "", "1", ""]
    expected = 304
    assert solution(inventory_list_test) == expected
