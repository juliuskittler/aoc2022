import pathlib
from typing import List


def solution(instructions: List[str]) -> int:
    # Initialize useful variables
    x = 1
    cycle = 1
    signal_strength = 1
    signal_strength_sum = 0
    signal_strength_cycles = [20, 60, 100, 140, 180, 220]

    # Loop through each instruction
    for instruction in instructions[0:150]:

        # Parse instruction
        if instruction == "noop":
            x_delta = 0
            cycle_delta = 1
        elif instruction[0:4] == "addx":
            x_delta = int(instruction.split(" ")[1])
            cycle_delta = 2

        # Compute and add signal strength to sum if necessary
        if cycle in signal_strength_cycles:
            # Current cycle is of interest
            signal_strength = cycle * x
            signal_strength_sum += signal_strength
        elif cycle_delta == 2 and cycle + 1 in signal_strength_cycles:
            # Next cycle is of interest but we will actually update by 2 cycles
            signal_strength = (cycle + 1) * x
            signal_strength_sum += signal_strength

        # Update cycle and x
        cycle += cycle_delta
        x += x_delta

    return signal_strength_sum


if __name__ == "__main__":

    filepath = pathlib.Path("10/input.txt")
    with open(filepath, "r") as f:
        instructions = f.read().splitlines()

    print(solution(instructions))  # expected: 15020

    # Test 1
    filepath = pathlib.Path("10/input_test_1.txt")
    with open(filepath, "r") as f:
        instructions_test = f.read().splitlines()
    expected = 13140
    assert solution(instructions_test) == expected
