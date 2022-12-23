from typing import List, Tuple


def print_map(elve_coords: List[Tuple[int]]):
    """Auxilary function to plot the map."""

    # Get the min_x, min_y, max_x, max_y coordinates to compute the size of the grid.
    # Subtract from that the number of elves to get the answer.
    i_coords = [i for i, _ in elve_coords]
    max_y = max(i_coords)
    min_y = min(i_coords)

    j_coords = [j for _, j in elve_coords]
    max_x = max(j_coords)
    min_x = min(j_coords)

    # Compute the dimensions of our map
    n_rows = max_y - min_y + 1
    n_cols = max_x - min_x + 1

    # Correct the elve coordinates so that they fit onto th emap
    elve_coords_print = []
    for (i, j) in elve_coords:
        elve_coords_print.append((i + abs(min_y), j + abs(min_x)))

    # Initialize an empty map
    map_print = [["." for j in range(n_cols)] for i in range(n_rows)]

    # Put the elve coordinates onto the map
    for (i, j) in elve_coords_print:
        map_print[i][j] = "#"

    # Print the map
    for row in map_print:
        print("".join(row))
