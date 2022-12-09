import pathlib
from typing import List

"""
Note: 
- The difficulty seems to be that we don't know the dimensions of 
the grid where the movements will take place up front. This makes it 
difficult to initialize the grid up-front as an actual grid. What we
could do is just use a set with the coordinates relative to the
starting point s. This seems the most space-efficient since we only
need to store positions that T has actually visited, not the ones that
it has not visited.
"""


def solution(head_motions: List[str]) -> int:

    # Initialize useful variables
    x_idx_h = 0  # x-axis position of head H
    y_idx_h = 0  # y-axis position of head H
    x_idx_t = 0  # x-axis position of tail T
    y_idx_t = 0  # y-axis position of tail T
    positions_of_t = set()  # positions visited by the tail T

    for motion in head_motions:

        # Parse the motion
        direction, steps = motion.split(" ")
        steps = int(steps)

        # For each step, we change the position of T and H
        # and add the position of T to positions_of_t
        for step in range(steps):

            # Change position of the head H
            if direction == "R":
                x_idx_h += 1
            elif direction == "L":
                x_idx_h -= 1
            elif direction == "D":
                y_idx_h += 1
            elif direction == "U":
                y_idx_h -= 1

            # Change position of the tail T

            # If they are in the same row and H is at least 2 steps away from T
            # -> Move T horizontally by 1 step.
            if y_idx_t == y_idx_h and abs(x_idx_t - x_idx_h) > 1:
                if x_idx_h > x_idx_t:  # if H is to the right of T, move T to the right
                    x_idx_t += 1
                elif x_idx_h < x_idx_t:  # if H is to the left of T, move T to the left
                    x_idx_t -= 1
            # If they are in the same column and H is at least 2 steps away from T
            # -> Move T vertically by 1 step.
            elif x_idx_t == x_idx_h and abs(y_idx_t - y_idx_h) > 1:
                if y_idx_h > y_idx_t:  # if H is to the bottom of T, move T down
                    y_idx_t += 1
                elif y_idx_h < y_idx_t:  # if H is to the top of T, move T up
                    y_idx_t -= 1
            # If they are in a different row or column and do not touch diagonally.
            # -> Move T diagonally.
            elif ((x_idx_t != x_idx_h) and (y_idx_t != y_idx_h)) and (
                (abs(x_idx_t - x_idx_h) > 1) or (abs(y_idx_t - y_idx_h) > 1)
            ):
                # Move up right
                if y_idx_h < y_idx_t and x_idx_h > x_idx_t:
                    y_idx_t -= 1
                    x_idx_t += 1
                # Move up left
                elif y_idx_h < y_idx_t and x_idx_h < x_idx_t:
                    y_idx_t -= 1
                    x_idx_t -= 1
                # Move down right
                elif y_idx_h > y_idx_t and x_idx_h > x_idx_t:
                    y_idx_t += 1
                    x_idx_t += 1
                # Move down left
                elif y_idx_h > y_idx_t and x_idx_h < x_idx_t:
                    y_idx_t += 1
                    x_idx_t -= 1
            # Do nothing if HT touch vertically, horizontally or diagonally.

            # Add the current position of T to positions_of_t.
            # (The current position of T will only be added if it's not yet in the set.)
            positions_of_t.add((x_idx_t, y_idx_t))

    number_of_positions_visited_by_t = len(positions_of_t)
    return number_of_positions_visited_by_t


if __name__ == "__main__":

    filepath = pathlib.Path("09/input.txt")
    with open(filepath, "r") as f:
        head_motions = f.read().splitlines()

    print(solution(head_motions))  # correct: 6311

    # Test 1
    head_motions_test = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]
    expected = 13
    assert solution(head_motions_test) == expected
