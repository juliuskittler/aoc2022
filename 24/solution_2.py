"""2022, day 24, part 2: https://adventofcode.com/2022/day/24.

My code from part 1 is essentially reused, just that we call the algorithm multiple
times with different start and end positions and sum up all the steps taken.
"""

import pathlib
from typing import Tuple

from utils import parse_inputs


class Solution:
    def __init__(self, filepath: pathlib.Path) -> None:
        # Read inputs
        (
            self.pos_dict,
            self.dir_dict,
            self.min_i,
            self.max_i,
            self.min_j,
            self.max_j,
        ) = parse_inputs(filepath)

        # Provide position deltas for each direction
        self.pos_delta = {
            ">": (0, 1),  # move right -> increase j by 1
            "<": (0, -1),  # move left  -> decrease j by 1
            "^": (-1, 0),  # move up    -> decrease i by 1
            "v": (1, 0),  # move down  -> increase i by 1
        }

    def _get_new_blizzard_pos(self, dir: str, pos: Tuple[int]) -> Tuple[int]:
        new_i = pos[0] + self.pos_delta[dir][0]
        new_j = pos[1] + self.pos_delta[dir][1]

        # Wrap around at top and bottom if needed
        if new_i > self.max_i:
            new_i = self.min_i
        elif new_i < self.min_i:
            new_i = self.max_i

        # Wrap around left and right if needed
        if new_j > self.max_j:
            new_j = self.min_j
        elif new_j < self.min_j:
            new_j = self.max_j

        return (new_i, new_j)

    def _get_new_person_pos(self, dir: str, pos: Tuple[int]) -> Tuple[int]:
        new_i = pos[0] + self.pos_delta[dir][0]
        new_j = pos[1] + self.pos_delta[dir][1]

        # Stop at top and bottom if needed
        if new_i > self.max_i:
            new_i = self.max_i
        elif new_i < self.min_i:
            new_i = self.min_i

        # Stop left and right if needed
        if new_j > self.max_j:
            new_j = self.max_j
        elif new_j < self.min_j:
            new_j = self.min_j

        return (new_i, new_j)

    def _get_steps_required(self, s_pos: Tuple[int], e_prev_pos: Tuple[int]) -> int:

        # Initialize useful variables
        self.prev_pos_set = {s_pos}  # set of positions at the previous step

        # Iterate until we have found a path to our final position final_pos
        step = 0
        path_found = False
        while not path_found:

            # Check termination condition
            if e_prev_pos in self.prev_pos_set:
                path_found = True

            # Iterate over each blizzard and update its position
            for idx, pos in self.pos_dict.items():
                dir, pos = self.dir_dict[idx], self.pos_dict[idx]
                self.pos_dict[idx] = self._get_new_blizzard_pos(dir, pos)

            # Keep a set of the current blizzard positions for convenience and speed
            blizzard_pos_set = set(self.pos_dict.values())

            # Update the set of our possible positions at the current step
            new_pos_set = set()
            for prev_pos in self.prev_pos_set:

                # Add previous position itself if there is no blizzard at current step
                if prev_pos not in blizzard_pos_set:
                    new_pos_set.add(prev_pos)
                # Check if we can go right, left, up, down from the current position
                for dir in self.pos_delta:
                    cand_pos = self._get_new_person_pos(dir, prev_pos)
                    if cand_pos not in blizzard_pos_set:
                        new_pos_set.add(cand_pos)
            self.prev_pos_set = new_pos_set

            # Update step
            step += 1

        return step

    def get_solution(self) -> int:

        # Initialize useful variables
        s_pos = (self.min_i - 1, self.min_j)  # start position
        s_prev_pos = (self.min_i, self.min_j)  # position just before start position
        e_pos = (self.max_i + 1, self.max_j)  # end position
        e_prev_pos = (self.max_i, self.max_j)  # position just before end position

        # Sum up the required number of steps
        steps = 0
        steps += self._get_steps_required(s_pos, e_prev_pos)  # start to end
        steps += self._get_steps_required(e_pos, s_prev_pos)  # end to start
        steps += self._get_steps_required(s_pos, e_prev_pos)  # start to end
        return steps


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(Solution(filepath).get_solution())  # correct: 794

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 54
    assert Solution(filepath).get_solution() == expected
