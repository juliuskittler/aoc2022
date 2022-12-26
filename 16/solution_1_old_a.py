import copy
import pathlib
from typing import Dict, List

from utils import get_valve_info


class Solution:
    def __init__(
        self,
        flow_rates: List[int],
        dest_valves: List[str],
        targ_valves: List[List[str]],
    ) -> None:
        # Initialize useful variables
        self.start_valve = dest_valves[0]
        self.start_minute = 0
        self.start_pressure = 0
        self.start_open_valves = []

        self.n_minutes = 30
        self.n_valves = len(dest_valves)
        self.max_pressure = 0
        self.cnt_trials = 0
        self.visited_cnt = {
            dv: 0 for dv in dest_valves
        }  # how many times we have visited each valve

        # Construct a full graph that points from destination valves to target valves
        self.graph = dict()
        for i in range(self.n_valves):
            self.graph[dest_valves[i]] = {
                "flow_rate": flow_rates[i],
                "target_valves": targ_valves[i],
            }

        # Sort the target_valves by their respective flow_rates descendingly
        for dest_valve in dest_valves:
            targ_valves = self.graph[dest_valve]["target_valves"]
            flow_rates = [self.graph[tv]["flow_rate"] for tv in targ_valves]
            targ_valves_sorted = [
                tv
                for tv, _ in sorted(
                    zip(targ_valves, flow_rates), key=lambda x: x[0], reverse=True
                )
            ]
            self.graph[dest_valve]["target_valves"] = targ_valves_sorted

    def get_solution(self) -> int:
        self.get_max_pressure(
            self.start_minute,
            self.start_valve,
            self.start_pressure,
            self.start_open_valves,
            self.visited_cnt,
        )
        return self.max_pressure

    def get_max_pressure(
        self,
        minute: int,
        valve: str,
        pressure: int,
        open_valves: List,
        visited_cnt: Dict,
    ):

        # Ensure that variables don't get overwritten
        minute = copy.deepcopy(minute)
        valve = copy.deepcopy(valve)
        pressure = copy.deepcopy(pressure)
        open_valves = copy.deepcopy(open_valves)

        # Increase minute by 1 (regardless of action: open valve or go to next valve)
        minute += 1

        # Increase pressure based on the valves that are already open
        pressure += sum(
            [self.graph[open_valve]["flow_rate"] for open_valve in open_valves]
        )

        # If time is out, update class variables
        if minute == self.n_minutes:
            self.cnt_trials += 1

            # Increase max_pressure if possible
            if pressure > self.max_pressure:
                self.max_pressure = pressure

            print("\ncnt_trials: {}".format(self.cnt_trials))
            print("max_pressure: {}".format(self.max_pressure))
            print("open_valves: {}".format(open_valves))

        # If time is not out, keep iterating
        elif minute < self.n_minutes:

            # Continue walking (this makes sense both if flow_rate > 0 and flow_rate == 0)
            for target_valve in self.graph[valve]["target_valves"]:

                # We only visit the target_valve if we have visited it at most once
                if visited_cnt[target_valve] <= 2:
                    visited_cnt_new = copy.deepcopy(visited_cnt)
                    visited_cnt_new[target_valve] += 1
                    self.get_max_pressure(
                        minute, target_valve, pressure, open_valves, visited_cnt_new
                    )

            # Open valve, then continue walking (this only makes sense if flow rate > 0)
            if self.graph[valve]["flow_rate"] > 0 and valve not in open_valves:

                # Simulate that we open the current valve by updating the values for
                # minute, pressure and open_valves
                minute_new = minute + 1
                pressure_new = pressure + sum(
                    [self.graph[open_valve]["flow_rate"] for open_valve in open_valves]
                )
                open_valves_new = open_valves + [valve]

                # Take the next step after opening the current valve
                for target_valve in self.graph[valve]["target_valves"]:

                    # We only visit the target_valve if we have visited it at most once
                    if visited_cnt[target_valve] <= 2:
                        visited_cnt_new = copy.deepcopy(visited_cnt)
                        visited_cnt_new[target_valve] += 1
                        self.get_max_pressure(
                            minute_new,
                            target_valve,
                            pressure_new,
                            open_valves_new,
                            visited_cnt_new,
                        )


if __name__ == "__main__":

    # filepath = pathlib.Path("16/input.txt")
    # flow_rates, dest_valves, targ_valves = get_valve_info(filepath)

    # print(solution(flow_rates, dest_valves, targ_valves))

    # Test 1
    filepath = pathlib.Path("16/input_test_1.txt")
    flow_rates_test, dest_valves_test, targ_valves_test = get_valve_info(filepath)
    expected = 1651
    print(Solution(flow_rates_test, dest_valves_test, targ_valves_test).get_solution())
    # assert solution(flow_rates_test, dest_valves_test, targ_valves_test) == expected
