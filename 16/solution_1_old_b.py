import copy
import pathlib
from typing import Dict, List

from utils import BreadthFirstSearch, get_valve_info


class Solution:
    def __init__(
        self,
        flow_rates: List[int],
        dest_valves: List[str],
        targ_valves: List[List[str]],
    ) -> None:
        # Initialize useful variables
        self.start_valve = "AA"
        self.start_minute = 0
        self.start_pressure = 0
        self.start_open_valves = []
        self.start_skipped_open = 0

        self.n_minutes = 30
        self.n_valves = len(dest_valves)
        self.max_pressure = 0

        # Construct a full graph that points from destination valves to target valves
        self.graph = dict()
        for i in range(self.n_valves):
            self.graph[dest_valves[i]] = targ_valves[i]

        # Construct a dictionary that contains the flow rate for each valve
        self.fr_dict = dict()
        for i in range(self.n_valves):
            self.fr_dict[dest_valves[i]] = flow_rates[i]

        # Get a set valves with positive flow_rates
        self.valves_pos = {valve for valve, fr in self.fr_dict.items() if fr > 0}

        # Get a set consisitng of start valve and valves with positive flow rates
        self.valves_red = self.valves_pos.union({self.start_valve})

    def _get_reduced_graph(self):
        """Obtain a graph of reduced valves.

        The reduced graph consists of start valve and valves with positive flow rate.
        """
        # Initalize reduced graph of start valve and all valves with non-zero flow rates
        self.graph_red = dict()

        # Iterate over the start valve and all valves with non-zero flow rates
        for source_valve in self.valves_red:

            # Get list of all potential target valves with positive flow rate
            target_valves = list(self.valves_pos - {source_valve})

            # Update the reduced graph
            self.graph_red[source_valve] = target_valves

    def _get_travel_cost(self):
        """Use BFS to find the travel cost between the nodes in the reduced graph.

        The travel cost is the number of steps (equivalent to the minutes passed) that
        are reqiured to travel from one valve to another. The resulting dict is stored
        as the class variable self.cost_red and can be queried with
        self.cost_red[source_valve][target_valve] to get the travel cost for moving
        from the specified source_valve to the specified target_valve.
        """
        # Initialize dict that holds the travel cost from source to target valve
        self.cost_red = dict()

        # Iterate over the start valve and all valves with non-zero flow rates
        for source_valve in self.valves_red:

            # Get list of all potential target valves with positive flow rate
            target_valves = list(self.valves_pos - {source_valve})

            # Traverse the graph with the source valve as starting point
            bfs = BreadthFirstSearch(self.graph)
            bfs.solve(source_valve)

            # Find the shortest paths from source valve to each of the target valve and
            # dd the length of the shortest path as cost to our cost dict.
            cost = {}
            for target_valve in target_valves:
                path = bfs.reconstruct_path(source_valve, target_valve)
                path_len = len(path)
                cost[target_valve] = path_len - 1  # -1 since we don't count start_valve
            self.cost_red[source_valve] = cost

    def _take_action(
        self,
        minute: int,
        valve: str,
        pressure: int,
        open_valves: List,
        skipped_open: int,
    ):
        # Ensure that variables don't get overwritten
        minute = copy.deepcopy(minute)
        valve = copy.deepcopy(valve)
        pressure = copy.deepcopy(pressure)
        open_valves = copy.deepcopy(open_valves)

        # From the current valve, visit all valves that are not yet open
        closed_valves = [v for v in self.graph_red[valve] if v not in open_valves]

        for target_valve in closed_valves:
            # Get cost of travelling to the respective valves
            cost = self.cost_red[valve][target_valve]

            # If we can still go to that valve in the given minutes, do that
            minutes_remaining = self.n_minutes - minute
            if minutes_remaining > cost:

                # Simulate time and pressure increases until target valve is reached
                pressure_new = pressure + cost * sum(
                    [self.fr_dict[open_valve] for open_valve in open_valves]
                )
                minute_new = minute + cost

                # Increase max_pressure if possible
                if pressure_new > self.max_pressure:
                    self.max_pressure = pressure_new
                    self.best_path = open_valves

                # From the next target valve, get the maximum pressure again
                self._get_max_pressure(
                    minute_new, target_valve, pressure_new, open_valves, skipped_open
                )

            # Otherwise, simply increase the pressure for the period until time is out
            else:
                # Simulate time and pressure increases until time is out
                pressure_new = pressure + minutes_remaining * sum(
                    [self.fr_dict[open_valve] for open_valve in open_valves]
                )

                # Increase max_pressure if possible
                if pressure_new > self.max_pressure:
                    self.max_pressure = pressure_new
                    self.best_path = open_valves
                    print(self.best_path)
                    print(self.max_pressure)

    def _get_max_pressure(
        self,
        minute: int,
        valve: str,
        pressure: int,
        open_valves: List,
        skipped_open: int,
    ):
        if skipped_open < 3:
            # Case where we DO NOT open the current valve
            skipped_open_new = skipped_open + 1
            self._take_action(minute, valve, pressure, open_valves, skipped_open_new)
        else:
            # Case where we open the current valve
            if valve != self.start_valve:
                open_valves_new = open_valves + [valve]
                minute_new = minute + 1
                skipped_open_new = 0
                self._take_action(
                    minute_new, valve, pressure, open_valves_new, skipped_open_new
                )

    def get_solution(self):

        # Reduce graph and get corresponding travel cost
        self._get_reduced_graph()
        self._get_travel_cost()
        # print(self.graph_red)
        # print(self.cost_red)

        self._get_max_pressure(
            self.start_minute,
            self.start_valve,
            self.start_pressure,
            self.start_open_valves,
            self.start_skipped_open,
        )
        print(self.best_path)
        return self.max_pressure


if __name__ == "__main__":

    # filepath = pathlib.Path("16/input.txt")
    # flow_rates, dest_valves, targ_valves = get_valve_info(filepath)

    # print(solution(flow_rates, dest_valves, targ_valves))

    # Test 1
    filepath = pathlib.Path("16/input_test_1.txt")
    flow_rates_test, dest_valves_test, targ_valves_test = get_valve_info(filepath)
    expected = 1651
    # Solution(flow_rates_test, dest_valves_test, targ_valves_test).get_solution()
    print(Solution(flow_rates_test, dest_valves_test, targ_valves_test).get_solution())
    # assert solution(flow_rates_test, dest_valves_test, targ_valves_test) == expected
