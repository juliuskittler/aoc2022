"""2022, day 1, part 2: https://adventofcode.com/2022/day/1."""
import pathlib


def solution(filepath: pathlib.Path, top_k: int = 3) -> int:

    with open(filepath, "r") as f:
        inventory_list = f.read().splitlines()

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

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 67622

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 45000
    assert solution(filepath) == expected
