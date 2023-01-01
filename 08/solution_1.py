"""2022, day 8, part 1: https://adventofcode.com/2022/day/8."""
import pathlib


def solution(filepath: pathlib.Path) -> int:

    with open(filepath, "r") as f:
        treegrid_str = f.read().splitlines()
        treegrid = []
        for treerow_str in treegrid_str:
            treerow = [int(height) for height in treerow_str]
            treegrid.append(treerow)

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

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 1859

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 21
    assert solution(filepath) == expected
