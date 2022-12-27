import copy
import pathlib
from typing import List

from utils import BreadthFirstSearch, get_valve_info

"""
Note: 
- The approach is as follows:
    - Reduce the graph to a graph that only consists of valves with positive flow rate.
    This is simply done by filtering out irrelevant valves.
    - Compute the travel cost for all pairs of valves in this reduced graph (i.e. how 
    many minutes does it take to travel from one valve to the other). This is done with
    Breadth First Search.
    - Recursively traverse the graph with a Depth First Search approach. I.e., we only 
    attempt new paths once we have reached a leaf node for the current path. The leaf
    node represents the maximum pressure that can be released with the current path.
    - The number of paths is huge. We have 15 valves with positive flow rates. Assuming
    all valves of all possible paths can be visited (without a time out), we have 
    factorial(15) paths that we would attempt to try out until there is a time out. 
    That's more than 1 trillion paths.
    - Therefore, we speed up the process with a trick. We still consider all paths but
    we take a shortcut whenever possible. We represent the current state with three
    elements: the current valve, the number of remaining minutes (after opening the
    current valve), the list of valves that are already open. Regardless of how we 
    reached this state, the best maximum pressure that can be reached from this state 
    will always be the same. We don't need to know the exact path that gives us this 
    maximum pressure. Instead, we only need to know the value of the maximum pressure. 
    So, we simply create a lookup dictionary that stores the maximum pressure for each 
    state that we have visited already. If the same state happens to be visited again, 
    then we simply return the maximum pressure of that state from the lookup table 
    instead of recursing down our graph and trying out all paths again.
"""


class Solution:
    def __init__(
        self,
        flow_rates: List[int],
        dest_valves: List[str],
        targ_valves: List[List[str]],
    ) -> None:
        # Initialize useful variables
        self.init_valve = "AA"
        self.init_rem_minutes = 30
        self.pressure_dict = dict()
        self.n_valves = len(dest_valves)

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
        self.n_valves_pos = len(self.valves_pos)

        # Get a set consisitng of start valve and valves with positive flow rates
        self.valves_red = self.valves_pos.union({self.init_valve})

        # Initialize an index for the valves with positive flow_rates
        self.valves_red_idx = {valve: i for i, valve in enumerate(self.valves_red)}
        self.init_open_valves = [0] * len(self.valves_red)

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
                cost[target_valve] = path_len - 1  # -1 since we don't count init_valve
            self.cost_red[source_valve] = cost

    def _get_max_pressure(self, valve, rem_minutes, open_valves):

        # Construct key
        key = (self.valves_red_idx[valve], rem_minutes, *open_valves)

        # Only recurse if we have not visited the current state yet
        if key not in self.pressure_dict:

            max_pressure = 0

            # Get list of neighbors of the current valve
            neighbors = self.graph_red[valve]

            # Filter down the list to neighbors that have not been opened yet
            neighbors_unvisited = [
                n for n in neighbors if not open_valves[self.valves_red_idx[n]]
            ]

            # For each neighbor, get the max pressure if we go to this neighbor
            for valve_new in neighbors_unvisited:
                rem_minutes_new = rem_minutes - self.cost_red[valve][valve_new] - 1
                if rem_minutes_new > 0:

                    # Pretend that valve_new is opened
                    open_valves_new = copy.deepcopy(open_valves)
                    open_valves_new[self.valves_red_idx[valve_new]] = 1

                    # Compute max presure if we were to go to the valve_new
                    max_pressure_cand = (
                        self._get_max_pressure(
                            valve_new, rem_minutes_new, open_valves_new
                        )
                        + self.fr_dict[valve_new] * rem_minutes_new
                    )

                    max_pressure = max(max_pressure, max_pressure_cand)

            # Save max pressure in our dict for other iterations
            self.pressure_dict[key] = max_pressure

        return self.pressure_dict[key]

    def get_solution(self):

        # Reduce graph and get corresponding travel cost
        self._get_reduced_graph()
        self._get_travel_cost()

        # Compute maximum pressure
        max_pressure = self._get_max_pressure(
            self.init_valve, self.init_rem_minutes, self.init_open_valves
        )
        return max_pressure


if __name__ == "__main__":

    filepath = pathlib.Path("16/input.txt")
    flow_rates, dest_valves, targ_valves = get_valve_info(filepath)

    print(
        Solution(flow_rates, dest_valves, targ_valves).get_solution()
    )  # correct: 1775

    # Test 1
    filepath = pathlib.Path("16/input_test_1.txt")
    flow_rates_test, dest_valves_test, targ_valves_test = get_valve_info(filepath)
    expected = 1651
    assert (
        Solution(flow_rates_test, dest_valves_test, targ_valves_test).get_solution()
        == expected
    )
