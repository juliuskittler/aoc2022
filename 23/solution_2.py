import pathlib
from typing import List

from utils import print_map


def solution(map: List[str], verbose: bool = False) -> int:

    # Convert the map into a set of elve coordinates, skipping the empty spaces
    elve_coords = set()
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == "#":
                elve_coords.add((i, j))
    n_elves = len(elve_coords)

    # Order of the elves
    move_seqs = [
        ["n", "s", "w", "e"],
        ["s", "w", "e", "n"],
        ["w", "e", "n", "s"],
        ["e", "n", "s", "w"],
    ]
    move_idx = 0
    move_idx_max = len(move_seqs) - 1

    # Order deltas
    dir_deltas = {
        "n": (-1, 0),
        "ne": (-1, 1),
        "nw": (-1, -1),
        "e": (0, 1),
        "w": (0, -1),
        "s": (1, 0),
        "se": (1, 1),
        "sw": (1, -1),
    }
    dir_keys = dir_deltas.keys()
    n_dirs = len(dir_keys)

    # Iterate until no elve wants to move
    complete = False
    round_idx = 0

    while not complete:

        # Initialize dict that maps current elve coordinates to new elve coordinates
        new_elve_coords = dict()

        # Initialize dict that mapes new elve coordinates to number of elves interested
        cnt_per_coord = dict()

        # Initialize count of elves that do not want to move anymore
        cnt_not_moving = 0

        # Check for every elve coord if it wants to move and where
        move_seq = move_seqs[move_idx]

        # Conduct step 1: find desired new position of each elve
        for coord in elve_coords:

            # Check if the current elve needs to move
            cand_coords = {
                k: (coord[0] + dir_deltas[k][0], coord[1] + dir_deltas[k][1])
                for k in dir_keys
            }
            cand_coords_free = {
                k: cand_coords not in elve_coords
                for k, cand_coords in cand_coords.items()
            }

            n_free_cand_coords = sum(cand_coords_free.values())

            if n_free_cand_coords == n_dirs:
                # Stop if the current elve does not need to move
                cnt_not_moving += 1
                new_coord = coord
            else:
                # Compute the coordinates
                found_new_coord = False
                for move in move_seq:
                    if move == "n":
                        if (
                            cand_coords_free["n"]
                            and cand_coords_free["ne"]
                            and cand_coords_free["nw"]
                        ):
                            new_coord = cand_coords["n"]
                            found_new_coord = True
                            break
                    elif move == "s":
                        if (
                            cand_coords_free["s"]
                            and cand_coords_free["se"]
                            and cand_coords_free["sw"]
                        ):
                            new_coord = cand_coords["s"]
                            found_new_coord = True
                            break
                    elif move == "w":
                        if (
                            cand_coords_free["w"]
                            and cand_coords_free["nw"]
                            and cand_coords_free["sw"]
                        ):
                            new_coord = cand_coords["w"]
                            found_new_coord = True
                            break
                    elif move == "e":
                        if (
                            cand_coords_free["e"]
                            and cand_coords_free["ne"]
                            and cand_coords_free["se"]
                        ):
                            new_coord = cand_coords["e"]
                            found_new_coord = True
                            break
                if not found_new_coord:
                    new_coord = coord

            # Add new coord and count to our dictionaries
            new_elve_coords[coord] = new_coord
            if new_coord not in cnt_per_coord:
                cnt_per_coord[new_coord] = 1
            else:
                cnt_per_coord[new_coord] += 1

        # Conduct step 2: find actual new position of each elf
        # If multiple elves want to move to a desired new position, none of them move.
        for old_coord, new_coord in new_elve_coords.items():
            if cnt_per_coord[new_coord] > 1:
                new_elve_coords[old_coord] = old_coord

        # Check termination condition: all elves do not want to move anymore
        # print("cnt_not_moving {} vs. n_elves {}".format(cnt_not_moving, n_elves))
        if cnt_not_moving == n_elves:
            complete = True

        # Update elve_coords for the next iteration
        elve_coords = set(
            new_elve_coords.values()
        )  # set conversion essential for speed

        # Update the order for the next iteration
        if move_idx == move_idx_max:
            move_idx = 0
        else:
            move_idx += 1

        # Update round index
        round_idx += 1

    # Print the final map if we're verbose
    if verbose:
        print_map(elve_coords)

    return round_idx


if __name__ == "__main__":

    filepath = pathlib.Path("23/input.txt")
    with open(filepath, "r") as f:
        map_test = f.read().splitlines()

    print(solution(map_test))  # correct: 1008

    # Test 1
    filepath = pathlib.Path("23/input_test_1.txt")
    with open(filepath, "r") as f:
        map_test = f.read().splitlines()
    expected = 4
    assert solution(map_test) == expected

    # Test 2
    filepath = pathlib.Path("23/input_test_2.txt")
    with open(filepath, "r") as f:
        map_test = f.read().splitlines()
    expected = 20
    assert solution(map_test) == expected
