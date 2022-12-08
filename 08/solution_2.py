import pathlib
from typing import List


def solution(treegrid: List[str]) -> int:

    # Initialize useful variables
    n_rows = len(treegrid)
    n_cols = len(treegrid[0])
    max_scenic_score = 0

    # The scenic score of any of the trees at the outer border
    # is 0. Hence, we don't compute their scenic score (and start
    # looping at 1 and end 1 step before the last row/column).
    for row_idx in range(1, n_rows - 1):
        for col_idx in range(1, n_cols - 1):
            # Identify the scenic score for the current tree
            tree_size = treegrid[row_idx][col_idx]

            # Look right
            dist_r = 1
            i = col_idx + 1
            while i < n_cols - 1 and treegrid[row_idx][i] < tree_size:
                dist_r += 1
                i += 1

            # Look left
            dist_l = 1
            i = col_idx - 1
            while i > 0 and treegrid[row_idx][i] < tree_size:
                dist_l += 1
                i -= 1

            # Look top
            dist_t = 1
            i = row_idx - 1
            while i > 0 and treegrid[i][col_idx] < tree_size:
                dist_t += 1
                i -= 1

            # Look down
            dist_d = 1
            i = row_idx + 1
            while i < n_rows - 1 and treegrid[i][col_idx] < tree_size:
                dist_d += 1
                i += 1

            # Compute scenic score
            scenic_score = dist_r * dist_l * dist_t * dist_d

            # Keep track of maximum scenic score
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    return max_scenic_score


if __name__ == "__main__":

    filepath = pathlib.Path("08/input.txt")
    with open(filepath, "r") as f:
        treegrid_str = f.read().splitlines()
        treegrid = []
        for treerow_str in treegrid_str:
            treerow = [int(height) for height in treerow_str]
            treegrid.append(treerow)

    print(solution(treegrid))  # correct: 332640

    # Test 1
    treegrid_test = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    expected = 8
    assert solution(treegrid_test) == expected
