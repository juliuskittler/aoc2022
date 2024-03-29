"""2022, day 16, part 2: https://adventofcode.com/2022/day/16.

- This takes a bit longer to run than part 1 but it still completes in 1 minute or so.
- In this part 2, we have only 26 instead of 30 minutes and we have another 'you',
namely an elephant, who helps traversing the graph and opening valves.
- The solution is to split the set of valves to be opened into 2 disjoint sets, meaning
that the elephant will visit only valves that you won't visit and vice versa. You and
the elephant both indepently decide in which order to visit these valves.
- So, essentially, we everything as before. The only changes are in the __init__
function, where init_rem_minutes is set to 26, and in the get_solution function.
- In the get_solution function, we iterate over all possible pairs of disjoint
sets to be visited by you and the elephant. For each pair, we call the _get_max_pressure
function twice, once for you (using your set) and once for the elephant (using the
elephant's set). Note that the "set of valves to visit" is encoded as open_valves
parameter, where we basically pretend that certain valves have already been visited
before and therefore should not be visited anymore by you or the elephant.
"""

import copy
import itertools
import pathlib

from utils import BreadthFirstSearch, get_valve_info


class Solution:
    def __init__(self, filepath: pathlib.Path) -> None:

        flow_rates, dest_valves, targ_valves = get_valve_info(filepath)

        # Initialize useful variables
        self.init_valve = "AA"
        self.init_rem_minutes = 26
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
        self.valves_red_idx = {valve: i + 1 for i, valve in enumerate(self.valves_pos)}
        self.valves_red_idx["AA"] = 0

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

        # Initialize useful variables
        max_pressure = 0

        # Divide the valves into all possible subsets: one for you, one for the elephant
        # For each subset-pair, let you and elephant independently find the best path.
        cnt = 0
        cnt_max = 2**self.n_valves_pos // 2
        for open_valves_you in itertools.product([0, 1], repeat=self.n_valves_pos):

            # Convert open_valves to list, attach open start valve at the beginning
            # and create the inverse open valves for the elephant
            open_valves_elephant = [0] + [1 if x == 0 else 0 for x in open_valves_you]
            open_valves_you = [0] + list(open_valves_you)

            # Compute the max pressure for you and the elephant separately, sum them up
            max_pressure_elephant = self._get_max_pressure(
                self.init_valve, self.init_rem_minutes, open_valves_elephant
            )
            max_pressure_you = self._get_max_pressure(
                self.init_valve, self.init_rem_minutes, open_valves_you
            )
            max_pressure_cand = max_pressure_elephant + max_pressure_you

            # Update max pressure if it's larger
            max_pressure = max(max_pressure, max_pressure_cand)

            # We only need to check the first half of the permutations because the
            # second half will be exactly the same, with the only difference that
            # it will appear as if the elephant is now you and you are now the
            # elephant. However, it does not really matter who is who. Therefore,
            # the first half is perfectly sufficient.
            cnt += 1
            if cnt >= cnt_max:
                break

        return max_pressure


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(Solution(filepath).get_solution())  # correct: 2351

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 1707
    assert Solution(filepath).get_solution() == expected
