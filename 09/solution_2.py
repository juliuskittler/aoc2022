"""2022, day 9, part 2: https://adventofcode.com/2022/day/9."""
import pathlib
from typing import List, Tuple


def get_new_idx_for_t(idx_t: Tuple[int], idx_h: Tuple[int]) -> Tuple[int]:
    """Get new position of a tail-knot relative to its head-knot."""
    x_idx_t, y_idx_t = idx_t
    x_idx_h, y_idx_h = idx_h

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
    return (x_idx_t, y_idx_t)


def solution(head_motions: List[str]) -> int:

    # Initialize useful variables
    n_knots = 10
    idx_knot = [
        (0, 0)
    ] * n_knots  # indices of all 10 knots (H, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    positions_of_t = set()  # positions visited by the last tail, 9

    for motion in head_motions:

        # Parse the motion
        direction, steps = motion.split(" ")
        steps = int(steps)

        # For each step, we change the position of H and all its tails.
        # We then add the position of the last tail, 9, to positions_of_t.
        for step in range(steps):

            # Change position of the head H, the first element in idx_knot
            x_idx_h, y_idx_h = idx_knot[0]
            if direction == "R":
                x_idx_h += 1
            elif direction == "L":
                x_idx_h -= 1
            elif direction == "D":
                y_idx_h += 1
            elif direction == "U":
                y_idx_h -= 1
            idx_knot[0] = (x_idx_h, y_idx_h)

            # Change positions of all tails
            for i in range(1, n_knots):
                idx_knot[i] = get_new_idx_for_t(
                    idx_t=idx_knot[i], idx_h=idx_knot[i - 1]
                )

            # Add the current position of the last tail, 9, to positions_of_t
            # (The current position of T will only be added if it's not yet in the set.)
            positions_of_t.add(tuple(idx_knot[-1]))

    number_of_positions_visited_by_t = len(positions_of_t)
    return number_of_positions_visited_by_t


if __name__ == "__main__":

    filepath = pathlib.Path("09/input.txt")
    with open(filepath, "r") as f:
        head_motions = f.read().splitlines()

    print(solution(head_motions))  # correct: 2482

    # Test 1
    head_motions_test = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]
    expected = 1
    assert solution(head_motions_test) == expected

    # Test 2
    head_motions_test = ["R 5", "U 8", "L 8", "D 3", "R 17", "D 10", "L 25", "U 20"]
    expected = 36
    assert solution(head_motions_test) == expected
