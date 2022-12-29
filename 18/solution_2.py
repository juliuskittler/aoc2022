"""2022, day 18, part 2.

- We are supposed to not count surfaces of encosed areas ("air pockets") this time.
- There are 2 possible approaches essentially:
    - a) identify all ENCLOSED areas of air cubes, compute the sum of the surface areas
    of lava that touches these enclosed areas and then subtract this sum from the 
    overall sum of all surface areas (computed in part 1)
    - b) identify the OPEN area of air cubes, compute the sum of the surface areas of
    lava that touches these open areas and that's the answer.
- Approach b) seems more easy to implement. This is mainly because in b) there is just 
1 open area whereas in a) there are multiple enclosed areas. If we have 1 open area 
where all air cubes are connected with each other through other air cubes, we can
use a recursive approach to build a set of all air cubes. (Each air cube is represented 
by a 3D coordinate.) In contrast, such a recursive approach would not work for a).
"""

import pathlib
import sys
from typing import Tuple

from utils import get_cubes

# Max recursion limit is at 1000 by default in Python. However, my recursive algorithm
# needs more than that. For the puzzle input, the deltas (max_x-min_x), (max_y-min_y),
# (max_z-min_z) are 21, 21, 20 respectively. Hence, I am setting the upper recursion
# limit to 21*21*20, which is the maximum size of our search space.
sys.setrecursionlimit(21 * 21 * 20)


class Solution:
    def __init__(self, filepath: pathlib.Path) -> None:

        # Store
        self.lava_cubes = set(get_cubes(filepath))
        self.air_cubes = set()

        # Identify the min and max coordinates for our air cubes
        min_lava_coords = map(min, zip(*self.lava_cubes))
        max_lava_coords = map(max, zip(*self.lava_cubes))
        self.min_x, self.min_y, self.min_z = (coord - 1 for coord in min_lava_coords)
        self.max_x, self.max_y, self.max_z = (coord + 1 for coord in max_lava_coords)

        # Initialize deltas to look up, down, right, left, in front, behind a cube
        self.deltas = [
            (0, +1, 0),  # up
            (0, -1, 0),  # down
            (+1, 0, 0),  # right
            (-1, 0, 0),  # left
            (0, 0, -1),  # in front
            (0, 0, +1),  # behind
        ]

    def find_air_cubes(self, air_cube: Tuple[int]) -> None:
        """Auxilary function to build the set of air cubes (self.air_cubes)"""
        # For each possible direction relative to the current air cube...
        for delta in self.deltas:

            # Identify candidate cube by shifting into one particular direction
            cand_cube = tuple(a + d for a, d in zip(air_cube, delta))

            # Check if the cand_cube already corresponds to an air cube or a lava cube
            if cand_cube in self.air_cubes or cand_cube in self.lava_cubes:
                continue

            # Check if the cand_cube has x, y or z coordinates beyond our min or max
            x_limit_breached = cand_cube[0] > self.max_x or cand_cube[0] < self.min_x
            y_limit_breached = cand_cube[1] > self.max_y or cand_cube[1] < self.min_y
            z_limit_breached = cand_cube[2] > self.max_z or cand_cube[2] < self.min_z
            if x_limit_breached or y_limit_breached or z_limit_breached:
                continue

            # Add cand_cube to our set of air cubes
            self.air_cubes.add(cand_cube)

            # Keep searching from this air cube
            self.find_air_cubes(cand_cube)

    def get_exterial_surface_area(self) -> int:
        """Auxilary function to count number of lava cube faces that touch air cubes."""
        exterial_surface_area = 0

        # For each lava cube...
        for lava_cube in self.lava_cubes:
            # For each possible direction relative to the current lava cube...
            for delta in self.deltas:
                # Identify candidate cube by shifting into one particular direction
                cand_cube = tuple(a + d for a, d in zip(lava_cube, delta))

                # If the candidate cube is an air cube, we increase our count by 1 since
                # it means that the current lava cube is touching an air cube there.
                if cand_cube in self.air_cubes:
                    exterial_surface_area += 1

        return exterial_surface_area

    def get_solution(self) -> int:

        # Build set of air cubes recursively, starting from the min air cube coordinates
        start_air_cube = (self.min_x, self.min_y, self.min_z)
        self.find_air_cubes(start_air_cube)

        # Compute result and return it
        exterial_surface_area = self.get_exterial_surface_area()
        return exterial_surface_area


if __name__ == "__main__":

    filepath = pathlib.Path("18/input.txt")
    print(Solution(filepath).get_solution())  # correct: 2060

    # Test 1
    filepath = pathlib.Path("18/input_test_1.txt")
    expected = 58
    assert Solution(filepath).get_solution() == expected

    # Test 2
    filepath = pathlib.Path("18/input_test_2.txt")
    expected = 30  # 6 connected sides -> 7 * 6 - 2*6
    assert Solution(filepath).get_solution() == expected
