"""2022, day 1, part 1: https://adventofcode.com/2022/day/1."""
import pathlib


def solution(filepath: pathlib.Path) -> int:

    with open(filepath, "r") as f:
        inventory_list = f.read().splitlines()

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

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 67622

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 24000
    assert solution(filepath) == expected
