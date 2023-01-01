"""2022, day 10, part 2: https://adventofcode.com/2022/day/10."""
import pathlib
from typing import List


def solution(filepath: pathlib.Path) -> int:

    with open(filepath, "r") as f:
        instructions = f.read().splitlines()

    # Initialize useful variables
    x = 1
    cycle = 1

    # We store the image since it's small
    cycles_total = 240
    cycles_per_row = 40
    n_rows = cycles_total // cycles_per_row
    image = ["."] * cycles_total

    # Loop through each instruction
    for instruction in instructions[0:150]:

        # Parse instruction
        if instruction == "noop":
            x_delta = 0
            cycle_delta = 1
        elif instruction[0:4] == "addx":
            x_delta = int(instruction.split(" ")[1])
            cycle_delta = 2

        # Draw a "#" in the image at the current cycle
        # if the index of the current cycle falls in the sprites,
        # i.e. in the indices [x-1, x, x+1] in the current row.
        for _ in range(cycle_delta):
            cycle_idx_in_current_row = (cycle - 1) % cycles_per_row
            cycle_in_sprites = cycle_idx_in_current_row in [x - 1, x, x + 1]
            if cycle_in_sprites:
                image[cycle - 1] = "#"
            cycle += 1

        # Update x
        x += x_delta

    # Print the image
    start_idx = 0
    for _ in range(n_rows):
        print("".join([image[i] for i in range(start_idx, start_idx + cycles_per_row)]))
        start_idx += cycles_per_row


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: EFUGLPAP

    ####.####.#..#..##..#....###...##..###..
    # ....#....#..#.#..#.#....#..#.#..#.#..#.
    ###..###..#..#.#....#....#..#.#..#.#..#.
    # ....#....#..#.#.##.#....###..####.###..
    # ....#....#..#.#..#.#....#....#..#.#....
    ####.#.....##...###.####.#....#..#.#....

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    solution(filepath)

    ##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######.....
