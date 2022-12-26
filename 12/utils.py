import string
from typing import Any, Dict, List, Tuple


def get_distance(letter_next: str, letter_curr: str) -> int:
    """Auxilary function to get the distance between 2 letters.

    Here the distance is defined as the number of 'letter steps'
    you have to take in order to move from one letter to another.
    E.g. from 'a' to 'b', it's one step (1), from 'b' to 'a' it's
    one step back (-1), from 'a' to 'c' it's two steps (2), from
    'c' to 'a' it's two steps back (-2) etc.
    """
    # E has the elevation of z, S has the elevation of a
    if letter_next == "E":
        letter_next = "z"
    elif letter_next == "S":
        letter_next = "a"
    if letter_curr == "S":
        letter_curr = "a"
    elif letter_curr == "E":
        letter_curr = "z"

    # Compute the distance
    letter_idx_next = string.ascii_lowercase.index(letter_next)
    letter_idx_curr = string.ascii_lowercase.index(letter_curr)
    distance = letter_idx_next - letter_idx_curr
    return distance


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
