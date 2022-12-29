"""2022, day 8, part 1."""
import pathlib
from typing import List


def solution(treegrid: List[str]) -> int:

    # Initialize useful variables
    n_rows = len(treegrid)
    n_cols = len(treegrid[0])
    is_visible_matrix = [[0] * n_cols for row in range(n_rows)]

    # Iterate over the grid 4 times: left -> right,
    # right -> left, top -> bottom, bottom -> top.
    # In each row/column we keep track of the largest
    # tree. If the current tree is larger, then we
    # mark in our is_visible_matrix that it is visible.

    # Horizontal pass
    for row_idx in range(n_rows):

        # Left -> right
        largest_tree = -1
        for col_idx in range(n_cols):
            tree_size = treegrid[row_idx][col_idx]
            if tree_size > largest_tree:
                is_visible_matrix[row_idx][col_idx] = 1
                largest_tree = tree_size

        # Right -> left
        largest_tree = -1
        for col_idx in reversed(range(n_cols)):
            tree_size = treegrid[row_idx][col_idx]
            if tree_size > largest_tree:
                is_visible_matrix[row_idx][col_idx] = 1
                largest_tree = tree_size

    # Vertical pass
    for col_idx in range(n_cols):

        # Top -> bottom
        largest_tree = -1
        for row_idx in range(n_rows):
            tree_size = treegrid[row_idx][col_idx]
            if tree_size > largest_tree:
                is_visible_matrix[row_idx][col_idx] = 1
                largest_tree = tree_size

        # Bottom -> top
        largest_tree = -1
        for row_idx in reversed(range(n_rows)):
            tree_size = treegrid[row_idx][col_idx]
            if tree_size > largest_tree:
                is_visible_matrix[row_idx][col_idx] = 1
                largest_tree = tree_size

    # Compute the sum of all elements in is_visible_matrix
    n_visible_trees = sum([sum(row) for row in is_visible_matrix])
    return n_visible_trees


if __name__ == "__main__":

    filepath = pathlib.Path("08/input.txt")
    with open(filepath, "r") as f:
        treegrid_str = f.read().splitlines()
        treegrid = []
        for treerow_str in treegrid_str:
            treerow = [int(height) for height in treerow_str]
            treegrid.append(treerow)

    print(solution(treegrid))  # correct: 1859

    # Test 1
    treegrid_test = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    expected = 21
    assert solution(treegrid_test) == expected
