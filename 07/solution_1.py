"""2022, day 7, part 1.

We make an important assumption about the order of the terminal outputs. The assumption
is that we only go a directory up if we have seen all files of the subdirectories.
"""

import pathlib
from typing import List


def solution(terminal_outputs: List[str]) -> int:

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

    # Sum up the directory size of directories with size of at most 100000
    sum_of_sizes = sum([size for size in size_per_dir if size <= 100000])
    return sum_of_sizes


if __name__ == "__main__":

    filepath = pathlib.Path("07/input.txt")
    with open(filepath, "r") as f:
        terminal_outputs = f.read().splitlines()

    print(solution(terminal_outputs))  # correct: 1432936

    # Test 1
    terminal_outputs_test = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]
    expected = 95437
    assert solution(terminal_outputs_test) == expected
