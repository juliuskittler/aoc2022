"""2022, day 8, part 2: https://adventofcode.com/2022/day/8."""
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

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 332640

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 8
    assert solution(filepath) == expected
