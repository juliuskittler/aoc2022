"""2022, day 7, part 2: https://adventofcode.com/2022/day/7."""

import pathlib


def solution(filepath: pathlib.Path) -> int:

    with open(filepath, "r") as f:
        terminal_outputs = f.read().splitlines()

    # Initialize useful variables
    size_per_dir = []  # For complete sums of filesizes for each directory
    pending_size_per_dir = []  # For incomplete sums of filesizes for each directory

    # Iterate through each output
    for output in terminal_outputs:
        if output.split(" ")[0].isdigit():
            # If the output contains a file size add it to the size of the current directory
            pending_size_per_dir[-1] += int(output.split(" ")[0])

        elif output == "$ cd ..":
            # If we go up one directory, we assume that we have seen all files of the
            # current directory and its subdirectories, i.e. we have summed up their sizes.
            size = pending_size_per_dir.pop()
            size_per_dir.append(size)

            # We also need to add the size to the next element in the stack since the size
            # of the current directory has to be added to the size of the parent directory.
            pending_size_per_dir[-1] += size

        elif output[0:4] == "$ cd":
            # If we go into any directory, we know that we need to add the size of one more
            # directory. Hence, we add an element to our stack. The element is 0 because
            # so far we don't know the file size of any of the files in this directory.
            pending_size_per_dir.append(0)

    # We add the size of the last directories if the stack is not empty.
    while len(pending_size_per_dir) > 1:
        size = pending_size_per_dir.pop()
        size_per_dir.append(size)
        pending_size_per_dir[-1] += size
    size = pending_size_per_dir.pop()
    size_per_dir.append(size)

    # Identify the smallest directory that, if deleted, would bring down the total
    # used storage to 40GB or less
    used_space_right_now = max(size_per_dir)  # size of the root directory
    total_available_space = 70000000
    free_space_right_now = total_available_space - used_space_right_now
    free_space_needed_for_update = 30000000
    min_space_to_remove = free_space_needed_for_update - free_space_right_now

    size_of_dir_to_remove = 100000000
    for size in size_per_dir:
        if size >= min_space_to_remove and size < size_of_dir_to_remove:
            size_of_dir_to_remove = size

    return size_of_dir_to_remove


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 272298

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 24933642
    assert solution(filepath) == expected
