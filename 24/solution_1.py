"""2022, day 24, part 1.

The solution consists of two main steps:
1. Constructing the blizzard field:
    - The positions of multiple blizzards can overlap at certain iterations. Therefore,
    I decided to keep track of the blizzard positions and their directions not with a 
    2D-array but instead with dictionaries. The key of the dictionaries is the index of 
    the blizzard. There are two dictionaries: one dictionary gives us the direction of 
    the respective blizzard and the other dictionary gives us the current position of 
    the respective blizzard.
    - Essentially, we need to iteratively change the positions of all blizzards based on 
    a) their direction and b) their current position. 1 iteration happens in 1 minute.
2. Finding the shortest path in the blizzard field:
    - Essentially, we want to find the shortest path from our starting position to our
    end position. Actually... we are not trying to find the shortest path but instead
    the path that takes the smallest possible number of minutes. Essentially, we can 
    stop at the minute when we find the first valid path.
    - To find the shortest path, we keep track of a set of valid positions at the
    current minute. In each minute, we update this set. Essentially, we fully replace 
    the current set with a new set. For each position in the current set, we look up 
    the valid next positions that are reachable from it. Then, we add these valid next 
    positions to the new set. Note that sometimes, a particular position may not be
    reflected in the new set at all because itself and all its sourrounding positions 
    may be covered by blizzards.
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
        e_prev_pos = (self.max_i, self.max_j)  # position just before end position

        return self._get_steps_required(s_pos, e_prev_pos)


if __name__ == "__main__":

    filepath = pathlib.Path("24/input.txt")
    print(Solution(filepath).get_solution())  # correct: 253

    # Test 1
    filepath = pathlib.Path("24/input_test_1.txt")
    expected = 18
    assert Solution(filepath).get_solution() == expected
