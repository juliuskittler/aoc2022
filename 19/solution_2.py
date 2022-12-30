"""2022, day 19, part 2.

- The solution is almost the same as for part 1, with the difference being only in
the function get_solution. Instead of 24 minutes, 32 minutes are made available.
Instead of all blueprints, only the first 3 blueprints are considered. Instead of
summing up the quality levels of the blueprints, the maximum number of geodes
of each of the blueprints are multiplied and returned as answer.
- The run time is longer than for part 1, it takes more than 1 minute. The test case
takes much longer to run than the puzzle case.
"""

import math
import pathlib
import re
from typing import Tuple


class Solution:
    def __init__(self, filepath: pathlib.Path, verbose: bool = False):

        self.verbose = verbose

        with open(filepath, "r") as f:
            blueprints = f.read().splitlines()
            self.blueprints = [
                list(map(int, re.findall("(-?\d+)", blueprint)))
                for blueprint in blueprints
            ]

    def get_max_geodes(self, key: Tuple[int]) -> int:

        # Check if the results have been cached
        if key in self.cache:
            return self.cache[key]

        # Extract information from key
        n_ore, n_cla, n_obs, n_geo, n_ore_r, n_cla_r, n_obs_r, n_geo_r, rem_mins = key

        # Stop if there is no time left
        if rem_mins == 0:
            return n_geo

        # We have 5 possible actions and need to return the maximum number of geodes
        # that can be returned with any of these: 1) do nothing, 2) produce geode robot,
        # 3) produce ore robot, 4) produce clay robot, 5) produce obsidian robot.
        max_geodes_list = list()

        # 1) Do nothing
        max_geodes_not = n_geo + n_geo_r * rem_mins
        max_geodes_list.append(max_geodes_not)

        # 2) Produce geode robot
        if n_obs_r > 0:  # requires at least 1 obsidian robot
            # Determine maximum amount of waiting time needed to produce geode robot
            wait_mins = max(
                [
                    math.ceil((self.ore_for_geo_r - n_ore) / n_ore_r),
                    math.ceil((self.obs_for_geo_r - n_obs) / n_obs_r),
                    0,
                ]
            )
            # Produce new geode robot, jumping to the time when it's available
            rem_mins_new = rem_mins - wait_mins - 1
            if rem_mins_new > 0:
                n_ore_new = n_ore + (wait_mins + 1) * n_ore_r - self.ore_for_geo_r
                n_cla_new = n_cla + (wait_mins + 1) * n_cla_r
                n_obs_new = n_obs + (wait_mins + 1) * n_obs_r - self.obs_for_geo_r
                n_geo_new = n_geo + (wait_mins + 1) * n_geo_r
                n_geo_r_new = n_geo_r + 1
                max_geodes_geo = self.get_max_geodes(
                    (
                        min(n_ore_new, self.max_ore * rem_mins_new),
                        min(n_cla_new, self.max_cla * rem_mins_new),
                        min(n_obs_new, self.max_obs * rem_mins_new),
                        n_geo_new,
                        n_ore_r,
                        n_cla_r,
                        n_obs_r,
                        n_geo_r_new,
                        rem_mins_new,
                    )
                )
                max_geodes_list.append(max_geodes_geo)

        # 3) Produce ore robot
        if n_ore_r < self.max_ore:
            # Determine maximum amount of waiting time needed to produce ore robot
            wait_mins = max([math.ceil((self.ore_for_ore_r - n_ore) / n_ore_r), 0])
            rem_mins_new = rem_mins - wait_mins - 1
            # Produce new ore robot, jumping to the time when it's available
            if rem_mins_new > 0:
                n_ore_new = n_ore + (wait_mins + 1) * n_ore_r - self.ore_for_ore_r
                n_cla_new = n_cla + (wait_mins + 1) * n_cla_r
                n_obs_new = n_obs + (wait_mins + 1) * n_obs_r
                n_geo_new = n_geo + (wait_mins + 1) * n_geo_r
                n_ore_r_new = n_ore_r + 1
                max_geodes_ore = self.get_max_geodes(
                    (
                        min(n_ore_new, self.max_ore * rem_mins_new),
                        min(n_cla_new, self.max_cla * rem_mins_new),
                        min(n_obs_new, self.max_obs * rem_mins_new),
                        n_geo_new,
                        n_ore_r_new,
                        n_cla_r,
                        n_obs_r,
                        n_geo_r,
                        rem_mins_new,
                    )
                )
                max_geodes_list.append(max_geodes_ore)

        # 4) Produce clay robot
        if n_cla_r < self.max_cla:
            # Determine maximum amount of waiting time needed to produce clay robot
            wait_mins = max([math.ceil((self.ore_for_cla_r - n_ore) / n_ore_r), 0])
            rem_mins_new = rem_mins - wait_mins - 1
            # Produce new clay robot, jumping to the time when it's available
            if rem_mins_new > 0:
                n_ore_new = n_ore + (wait_mins + 1) * n_ore_r - self.ore_for_cla_r
                n_cla_new = n_cla + (wait_mins + 1) * n_cla_r
                n_obs_new = n_obs + (wait_mins + 1) * n_obs_r
                n_geo_new = n_geo + (wait_mins + 1) * n_geo_r
                n_cla_r_new = n_cla_r + 1
                max_geodes_cla = self.get_max_geodes(
                    (
                        min(n_ore_new, self.max_ore * rem_mins_new),
                        min(n_cla_new, self.max_cla * rem_mins_new),
                        min(n_obs_new, self.max_obs * rem_mins_new),
                        n_geo_new,
                        n_ore_r,
                        n_cla_r_new,
                        n_obs_r,
                        n_geo_r,
                        rem_mins_new,
                    )
                )
                max_geodes_list.append(max_geodes_cla)

        # 5) Produce obsidian robot
        if n_obs_r < self.max_obs and n_cla_r > 0:  # requires at least 1 clay robot
            # Determine maximum amount of waiting time needed to produce obsidian robot
            wait_mins = max(
                [
                    math.ceil((self.ore_for_obs_r - n_ore) / n_ore_r),
                    math.ceil((self.cla_for_obs_r - n_cla) / n_cla_r),
                    0,
                ]
            )
            rem_mins_new = rem_mins - wait_mins - 1
            # Produce new obsidian robot, jumping to the time when it's available
            if rem_mins_new > 0:
                n_ore_new = n_ore + (wait_mins + 1) * n_ore_r - self.ore_for_obs_r
                n_cla_new = n_cla + (wait_mins + 1) * n_cla_r - self.cla_for_obs_r
                n_obs_new = n_obs + (wait_mins + 1) * n_obs_r
                n_geo_new = n_geo + (wait_mins + 1) * n_geo_r
                n_obs_r_new = n_obs_r + 1
                max_geodes_obs = self.get_max_geodes(
                    (
                        min(n_ore_new, self.max_ore * rem_mins_new),
                        min(n_cla_new, self.max_cla * rem_mins_new),
                        min(n_obs_new, self.max_obs * rem_mins_new),
                        n_geo_new,
                        n_ore_r,
                        n_cla_r,
                        n_obs_r_new,
                        n_geo_r,
                        rem_mins_new,
                    )
                )
                max_geodes_list.append(max_geodes_obs)

        # Return and cache the maximum number of geodes across all 5 options
        max_geodes = max(max_geodes_list)
        self.cache[key] = max_geodes
        return max_geodes

    def get_solution(self) -> int:

        product_of_max_geodes = 1
        for blueprint in self.blueprints[0:3]:

            # Extract relevant information as blueprints and store it as class variable
            (
                self.blueprint_id,
                self.ore_for_ore_r,  # Ore that we need to spend for an ore robot
                self.ore_for_cla_r,  # Ore that we need to spend for a clay robot
                self.ore_for_obs_r,  # Ore that we need to spend for an obsidian robot
                self.cla_for_obs_r,  # Clay that we need to spend for an obsidian robot
                self.ore_for_geo_r,  # Ore that we need to spend for a geode robot
                self.obs_for_geo_r,  # Obsidian that we need to spend for a geode robot
            ) = blueprint

            # Compute maximum resource that we can spend per iteration for any robot.
            self.max_ore = max(
                [
                    self.ore_for_ore_r,
                    self.ore_for_cla_r,
                    self.ore_for_obs_r,
                    self.ore_for_geo_r,
                ]
            )
            self.max_cla = self.cla_for_obs_r
            self.max_obs = self.obs_for_geo_r

            # Initialize cache for the current blueprint
            self.cache = {}

            # Recursively get the maximum number of geodes (start with 1 obsidian robot,
            # 32 minutes remaining)
            key = (0, 0, 0, 0, 1, 0, 0, 0, 32)
            max_geodes = self.get_max_geodes(key)

            # Update product
            product_of_max_geodes *= max_geodes

            # Print status if required
            if self.verbose:
                print("{}: {} geodes".format(self.blueprint_id, max_geodes))

        return product_of_max_geodes


if __name__ == "__main__":

    filepath = pathlib.Path("19/input.txt")
    print(Solution(filepath).get_solution())  # correct: 8250

    # Test 1
    filepath = pathlib.Path("19/input_test_1.txt")
    expected = 56 * 62
    assert Solution(filepath).get_solution() == expected
