import pathlib
import re
from typing import Any, Dict, List


def get_valve_info(filepath: pathlib.Path) -> List[List]:
    """Auxilary function to return a list of three lists.

    The three lists are [flow_rates, dest_valves, targ_valves].
    """
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

        flow_rates = list()
        dest_valves = list()
        targ_valves = list()

        for line in lines:

            # Extract data
            flow_rate = int(re.findall("flow rate=(-?\d+)", line)[0])
            dest_valve = line.split(" ")[1]

            if "lead to valves" in line:
                targ_valve = line.split("lead to valves ")[1].split(", ")
            elif "leads to valve" in line:
                targ_valve = [line.split("leads to valve ")[1]]

            # Store data in a list
            flow_rates.append(flow_rate)
            dest_valves.append(dest_valve)
            targ_valves.append(targ_valve)

    return [flow_rates, dest_valves, targ_valves]


class BreadthFirstSearch:
    """Breadth first search (BFS).

    This class implements two functionalities. The 'solve' function traverses the graph
    with breadth first search starting from a given start_node. The 'reconstruct_path'
    function returns the shortest path from a given start_node to a given end_node.
    Reference: https://www.youtube.com/watch?v=oDqjPvD54Ss&t=4s
    """

    def __init__(self, graph: Dict[Any, List[Any]]) -> None:
        """The graph is a dictionary of 'from' nodes pointing to 'to' nodes.

        Each key in the dictionary is a 'from' node. The corresponding value in the
        dictionary is a list of 'to' nodes. The nodes can be of any type (e.g. str,
        tuple, int) but all nodes need to be of the same type.
        """
        # Save graph as class variable
        self.graph = graph

        # Get the number of unique nodes
        from_nodes = list(self.graph.keys())
        to_nodes = [node for sublist in self.graph.values() for node in sublist]
        self.unique_nodes = set(from_nodes + to_nodes)
        self.n_nodes = len(self.unique_nodes)

    def solve(self, start_node: Any) -> None:
        """Traverse the graph with BFS approach (required for reconstruct_path.)

        This function does not return anything but saves the 'previous' dict as class
        variable so that it can be used by subsequent calls of the 'reconstruct_path'
        function. Moreover, it stores the 'iter' dict as class variable, which can be
        used to find out in which iteration a particular node was visited.
        """
        # Initialize queue
        queue = list()  # Use list as queue. Use .append to enqueue, .pop(0) to dequeue.
        queue.append(start_node)

        # Initialize dict about visited nodes.
        # Key is node, value is boolean indicating if node was visited.
        visited = {node: False for node in self.unique_nodes}

        # Initialize dict about previous nodes.
        # Key is node, value is node representing the previous node that was visited.
        self.previous = {node: None for node in self.unique_nodes}

        # Initialize dict about iteration
        # Key is node, value is the iteration at which this node was visited.
        self.iter = {node: None for node in self.unique_nodes}

        # Traverse graph until all nodes are visited
        i = 0
        while len(queue) > 0:
            node = queue.pop(0)
            neighbour_nodes = self.graph[node]

            for neighbour_node in neighbour_nodes:
                if not visited[neighbour_node]:
                    queue.append(neighbour_node)
                    visited[neighbour_node] = True
                    self.previous[neighbour_node] = node
                    self.iter[neighbour_node] = i
                    i += 1

        return None

    def reconstruct_path(self, start_node: Any, end_node: Any) -> List[Any]:
        """Returns the shortest path from a start to an end node as a list of nodes."""

        # Check if the solve function was already run.
        if not hasattr(self, "previous"):
            raise ValueError("Need to run solve function before reconstruct_path.")

        # Reconstruct path going backwards from end_node
        current_node = end_node
        path = [current_node]
        while current_node is not start_node:
            current_node = self.previous[current_node]
            path.append(current_node)

        # Reverse the path so that it starts at start_node and ends at end_node.
        path.reverse()

        # Return path if start_node and end_node are connected, else return empty list.
        if path[0] == start_node:
            return path
        else:
            return list()
