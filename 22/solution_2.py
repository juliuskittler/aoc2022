import pathlib
from typing import List, Union

from utils import get_instructions, get_map

"""Note: 
- The following algorithm scetch could potentially be used (illustrated in example_2.pdf). 
- However, I did not take the time to implement it in a way that generalizes to 
different cube shapes. Instead, I kind of cheated and hard-coded the mapping.
- The idea for an algorithm I would use if I had to implement it in a generalizable way:
- 1. We start by mapping edges that are connected at 1 point and have a 90 degree angle 
between them.
- 2. We proceeed by mapping edges that point in the same direction (e.g. both right, 
both left, both up or both down) and have all edges between them connected with each
other in some way (during step 1 or step 2.)
- 3. We proceed by mapping edges that point in the opposite direction (e.g. up and down
or left and right) and have all edges between them already connected with each other 
in some way (during step 1 or step 2.)
- 4. Connect the remaining sides to the other sides that are closest to them.
"""


def solution(
    map: List[List[str]], instructions: List[Union[str, int]], verbose: bool = False
) -> int:

    # Initialize dimenions
    n_rows = len(map)
    n_cols = len(map[0])

    # Initialize mapper to get the new direction
    new_direction = {
        "r": {
            "L": "u",  # if we look right, turn counter-clockwise, we look up (u)
            "R": "d",  # if we look right, turn clockwise, we look down (d)
        },
        "d": {
            "L": "r",  # if we look down, turn counter-clockwise, we look right (r)
            "R": "l",  # if we look down, turn clockwise, we look left (l)
        },
        "l": {
            "L": "d",  # if we look left, turn counter-clockwise, we look down (d)
            "R": "u",  # if we look left, turn clockwise, we look up ()
        },
        "u": {
            "L": "l",  # if we look up, turn counter-clockwise, we look left (l)
            "R": "r",  # if we look up, turn clockwise, we look right (r)
        },
    }

    # Initialize mapper to change x position depending on the direction
    new_x_delta = {"u": 0, "d": 0, "r": 1, "l": -1}

    # Initialize mapper to change y position depending on the direction
    new_y_delta = {"u": -1, "d": 1, "r": 0, "l": 0}

    # Get the length of the sides of the cube
    dim = 10e12
    for i in range(1, n_rows - 1):
        dim_cand = len([j for j in range(1, n_cols - 1) if map[i][j] != " "])
        if dim_cand < dim:
            dim = dim_cand
    for j in range(1, n_cols - 1):
        dim_cand = len([i for i in range(1, n_rows - 1) if map[i][j] != " "])
        if dim_cand < dim:
            dim = dim_cand

    # Mapper from current position to new position and new direction
    mapper_dict = dict()
    v1 = [(1, j) for j in range(1 + dim, 1 + dim * 2)]
    v2 = [(i, 1) for i in range(1 + dim * 3, 1 + dim * 4)]
    for i in range(dim):
        mapper_dict[v1[i]] = {"new_pt": v2[i], "new_d": "r"}
        mapper_dict[v2[i]] = {"new_pt": v1[i], "new_d": "d"}

    v3 = [(i, dim + 1) for i in range(1, 1 + dim)]
    v4 = list(reversed([(i, 1) for i in range(1 + dim * 2, 1 + dim * 3)]))
    for i in range(dim):
        mapper_dict[v3[i]] = {"new_pt": v4[i], "new_d": "r"}
        mapper_dict[v4[i]] = {"new_pt": v3[i], "new_d": "r"}

    v5 = [(i, dim + 1) for i in range(1 + dim, 1 + dim * 2)]
    v6 = [(dim * 2 + 1, j) for j in range(1, 1 + dim)]
    for i in range(dim):
        mapper_dict[v5[i]] = {"new_pt": v6[i], "new_d": "d"}
        mapper_dict[v6[i]] = {"new_pt": v5[i], "new_d": "r"}

    v7 = [(1, j) for j in range(1 + dim * 2, 1 + dim * 3)]
    v8 = [(dim * 4, j) for j in range(1, 1 + dim)]
    for i in range(dim):
        mapper_dict[v7[i]] = {"new_pt": v8[i], "new_d": "u"}
        mapper_dict[v8[i]] = {"new_pt": v7[i], "new_d": "d"}

    v9 = [(dim * 3, j) for j in range(1 + dim, 1 + dim * 2)]
    v10 = [(i, dim) for i in range(1 + dim * 3, 1 + dim * 4)]
    for i in range(dim):
        mapper_dict[v9[i]] = {"new_pt": v10[i], "new_d": "l"}
        mapper_dict[v10[i]] = {"new_pt": v9[i], "new_d": "u"}

    v11 = [(dim, j) for j in range(1 + dim * 2, 1 + dim * 3)]
    v12 = [(i, dim * 2) for i in range(1 + dim, 1 + dim * 2)]
    for i in range(dim):
        mapper_dict[v11[i]] = {"new_pt": v12[i], "new_d": "l"}
        mapper_dict[v12[i]] = {"new_pt": v11[i], "new_d": "u"}

    v13 = [(i, dim * 3) for i in range(1, 1 + dim)]
    v14 = list(reversed([(i, dim * 2) for i in range(1 + dim * 2, 1 + dim * 3)]))
    for i in range(dim):
        mapper_dict[v13[i]] = {"new_pt": v14[i], "new_d": "l"}
        mapper_dict[v14[i]] = {"new_pt": v13[i], "new_d": "l"}

    # Initialize the x- and y-indices and direction at the beginning
    y = 1
    x = [j for j in range(1, n_cols - 1) if map[1][j] != " "][
        0
    ]  # 1st non-space element
    d = "r"

    # Traverse the map as specified by the instructions
    for inst in instructions:
        # Update the direction if needed
        if inst in ["L", "R"]:
            d = new_direction[d][inst]
        # Update the position if needed
        else:
            # Make as many steps as specified
            if verbose:
                print("\nMoving {} for {} steps:".format(d, inst))
            for _ in range(inst):

                # Get new candidate position
                x_cand = x + new_x_delta[d]
                y_cand = y + new_y_delta[d]

                # Wrap around and change direction if needed
                if map[y_cand][x_cand] == " ":
                    y_cand, x_cand = mapper_dict[(y, x)]["new_pt"]
                    d_cand = mapper_dict[(y, x)]["new_d"]
                    if map[y_cand][x_cand] != "#":
                        y = y_cand
                        x = x_cand
                        d = d_cand
                # Else don't wrap around and take a step if we can
                elif map[y_cand][x_cand] != "#":
                    y = y_cand
                    x = x_cand

                if verbose:
                    print("y: {}, x: {}".format(y, x))

    # Compute and return result
    d_constant = {"r": 0, "d": 1, "l": 2, "u": 3}
    result = 1000 * y + 4 * x + d_constant[d]
    return result


if __name__ == "__main__":

    filepath = pathlib.Path("22/input.txt")
    map = get_map(filepath)
    instructions = get_instructions(filepath)
    print(solution(map, instructions))  # correct: 144012
