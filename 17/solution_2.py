"""2022, day 17, part 2.

See solution_2.ipynb for explanation.
"""
import pathlib

from utils import get_shape_coords


def solution(dir_str: str, n_rocks: int = 10000) -> int:

    # Initialize useful variables
    x_start_coord = 2  # x-position where the rock starts falling
    y_start_delta = 4  # how many y-coordinates above the last rock the new rock falls
    x_tunnel_min = 0  # the tunnel's leftmost coordinate is 0, left of that is a wall
    x_tunnel_max = 6  # the tunnel's rightmost coordinate is 6, right of that is a wall
    shape_order = ["-", "+", "L", "I", "box"]  # order in which the shapes fall
    shape_width_dict = {"-": 4, "+": 3, "L": 3, "I": 1, "box": 2}
    n_shapes = len(shape_order)  # number of shapes
    dir_str_idx_max = len(dir_str) - 1
    dir_str_idx = 0

    # We represent the shapes as lists...
    tunnel_coords = set()
    y_tunnel_max = 0

    # Keep delta of y_shape_max from round to round in a list
    y_tunnel_max_deltas = list()

    # For each rock that falls...
    for r in range(n_rocks):

        # Get the shape of the current rock
        shape_idx = r % n_shapes
        shape = shape_order[shape_idx]

        # Get the leftmost and rightmost coordinate of the current shape
        lm_coord = x_start_coord
        rm_coord = x_start_coord + shape_width_dict[shape] - 1

        # Change coordinate 4 times until the lowest coordinate of the rock is 1 level
        # above the level where there must be at least 1 position filled with a rock.
        for _ in range(y_start_delta):
            # Move to the right
            direction = dir_str[dir_str_idx]
            if direction == ">" and rm_coord < x_tunnel_max:
                rm_coord += 1
                lm_coord += 1
            # Move to the left
            elif direction == "<" and lm_coord > x_tunnel_min:
                rm_coord -= 1
                lm_coord -= 1
            # Update the dir_str_idx
            if dir_str_idx == dir_str_idx_max:
                dir_str_idx = 0
            else:
                dir_str_idx += 1

        # Get the coordinates of the current shape
        shape_coords = get_shape_coords(shape, y_tunnel_max, lm_coord)

        # See if we can move down. If not, then stop
        can_move_down = True
        while can_move_down:
            # New coordinates if we were to move down by 1
            shape_coords_cand = {(coord[0], coord[1] - 1) for coord in shape_coords}

            # All new coordinates must have y >= 0 and they must fit in the tunnel
            can_move_down = len(
                shape_coords_cand.intersection(tunnel_coords)
            ) == 0 and all([coord[1] >= 1 for coord in shape_coords_cand])
            if can_move_down:
                # Move the rock down
                shape_coords = shape_coords_cand
            else:
                # Land the rock in the tunnel
                tunnel_coords = tunnel_coords.union(shape_coords)

                # Update y_tunnel_max with the larget y-coordinate of the current shape
                y_shape_max = max([coord[1] for coord in shape_coords])

                # Print delta from current y_tunnel_max to y_tunnel_max
                y_tunnel_max_new = max([y_shape_max, y_tunnel_max])
                y_tunnel_max_deltas.append(y_tunnel_max_new - y_tunnel_max)

                # Update y_tunnel_max
                y_tunnel_max = y_tunnel_max_new

                break  # will break in the next iteration

            # Move the direction if possible
            # Move to the right
            if dir_str[dir_str_idx] == ">" and rm_coord < x_tunnel_max:
                shape_coords_cand = {(coord[0] + 1, coord[1]) for coord in shape_coords}
                can_move_right = len(shape_coords_cand.intersection(tunnel_coords)) == 0
                if can_move_right:
                    shape_coords = shape_coords_cand
                    rm_coord += 1
                    lm_coord += 1
            # Move to the left
            elif dir_str[dir_str_idx] == "<" and lm_coord > x_tunnel_min:
                shape_coords_cand = {(coord[0] - 1, coord[1]) for coord in shape_coords}
                can_move_left = len(shape_coords_cand.intersection(tunnel_coords)) == 0
                if can_move_left:
                    shape_coords = shape_coords_cand
                    rm_coord -= 1
                    lm_coord -= 1
            # Update the dir_str_idx
            if dir_str_idx == dir_str_idx_max:
                dir_str_idx = 0
            else:
                dir_str_idx += 1

    # # Debugging: Draw the tunnel. If you set n_rocks=10, the tunnel should look like
    # # the last tunnel image from the example in the problem statement.
    # tunnel_matrix = [["." for _ in range(x_tunnel_max+1)] for _ in range(y_tunnel_max+1)]
    # for i in range(y_tunnel_max+1):
    #     for j in range(x_tunnel_max+1):
    #         if (j, i) in tunnel_coords:
    #             tunnel_matrix[i][j] = "#"

    # for row in list(reversed(tunnel_matrix))[:-1]:
    #     print("|" + "".join(row) + "|")
    # print("+-------+")

    print(y_tunnel_max_deltas)

    # Return y_tunnel_max
    return y_tunnel_max


if __name__ == "__main__":

    filepath = pathlib.Path("17/input.txt")
    with open(filepath, "r") as f:
        dir_str = f.read()

    solution(dir_str)
