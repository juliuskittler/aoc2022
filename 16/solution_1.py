import copy
import pathlib
from itertools import permutations
from typing import Dict, List

from utils import BreadthFirstSearch, get_valve_info


class Solution:
    def __init__(
        self,
        flow_rates: List[int],
        dest_valves: List[str],
        targ_valves: List[List[str]],
        verbose: bool = False,
    ) -> None:
        # Initialize useful variables
        self.verbose = verbose
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

    def _get_max_pressure(self):

        # Consider all possible orders of the positive valves
        n_valves_pos = len(self.valves_pos)
        valve_seqs = permutations(self.valves_pos, n_valves_pos)

        for valve_seq in valve_seqs:

            # Initialize useful variables
            valve_seq = ["AA"] + list(valve_seq)  # Add starting point AA
            valves_opened = 0
            pressure_per_minute = 0
            pressure = 0
            minute = 0

            # Visit and open remaining valves
            for j, valve in enumerate(valve_seq[1:]):

                # Check if we already have a solution

                # Check if the limit is exceeded
                minutes_remaining = self.n_minutes - minute
                cost = self.cost_red[valve_seq[j]][valve] + 1

                # Continue if there is enough time to reach the next valve
                if cost <= minutes_remaining:
                    pressure += cost * pressure_per_minute
                    minute += cost
                    pressure_per_minute += self.fr_dict[valve]
                    valves_opened += 1
                # Only increase pressure if there is not enough time to reach next valve
                else:
                    pressure += minutes_remaining * pressure_per_minute

            # If all valves have been visited and there is still time, increase pressure
            minutes_remaining = self.n_minutes - minute
            all_valves_opened = valves_opened == n_valves_pos
            if all_valves_opened and minutes_remaining > 0:
                pressure += minutes_remaining * pressure_per_minute

            # Check if we can increase the pressure
            if pressure > self.max_pressure:
                self.max_pressure = pressure

    def get_solution(self):

        # Reduce graph and get corresponding travel cost
        self._get_reduced_graph()
        self._get_travel_cost()

        self._get_max_pressure()
        return self.max_pressure


if __name__ == "__main__":

    # filepath = pathlib.Path("16/input.txt")
    # flow_rates, dest_valves, targ_valves = get_valve_info(filepath)

    # print(Solution(flow_rates, dest_valves, targ_valves).get_solution())

    # Test 1
    filepath = pathlib.Path("16/input_test_1.txt")
    flow_rates_test, dest_valves_test, targ_valves_test = get_valve_info(filepath)
    expected = 1651
    assert (
        Solution(flow_rates_test, dest_valves_test, targ_valves_test).get_solution()
        == expected
    )
