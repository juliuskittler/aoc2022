import pathlib
from typing import Optional, Tuple

from utils import get_cubes

"""
Note:
- Each cube has 6 sides. We have to count the total number of sides that
are visible from outside.
- For instance, if we have 1,1,1 and 2,1,1, then we have 2 cubes lying right next to 
each on ther on the x-axis but they have the same coordinates on the y-axis
and on the z-axis. Hence, 2 sides are connected since the 2 cubes lie next to each
other. So the total number of visible sides is: 6+6-2=10
- Since the cubes all have the same size (1x1x1 cubes), 2 cubes can be connected on
at most 2 sides. For example, if we want to fully cover up a particular cube, we need 6 
additional cubes: (1,1,1) can be covered up with the cubes:
    - (0, 1, 1) # lies to the left on the x-axis
    - (2, 1, 1) # lies to the right on the x-axis
    - (1, 0, 1) # lies below on the y-axis
    - (1, 2, 1) # lies above on the y-axis
    - (1, 1, 0) # lies in front on the z-axis
    - (1, 1, 2) # lies behind on the z-axis
- What we really need as input is: the total number of cubes, the total number of sides
that are connected. Then, we can compute the answer as:
    - 6 * number of cubes - total number of connected sides
- Computing the total number of connected sides is the tricky part of this problem. We
know that 2 cubes are connected on a single side if
    - a) they have the same value on 2 axes,
    - b) they have a delta of 1 on the 3rd axis.
- Approach: 
    - Sort by x-axis, y-axis, z-axis (in this order), then iterate over the cubes and 
    count the number of subsequent pairs that are connected on a side.
    - Sort by x-axis, z-axis, y-axis (in this order) then do the same.
    - Sort by z-axis, y-axis, x-axis (in this order), then do the same. 
- What was not clear to me is the case when we have "hidden inner holes". E.g. we 
could have an empty area that is fully covered by other cubes. Do we count the inner
surface area into our overall count or not? It turns out that we do count the inner
surface area just like the outside surface area (based on the test case).
- Note: Afterwards, I read about alternative solutions and I found this one, which I 
really like: https://www.youtube.com/watch?v=7tlWvZTPz1c
"""


def count_connected_sides(ax: int, cubes: Tuple[int], n_cubes: Optional[int] = None):

    # Initialize useful variables
    if n_cubes == None:
        n_cubes = len(cubes)
    adjacent_count = 0

    # Sort by the axes in the specified order
    ax_equal = [axis for axis in range(3) if axis != ax]
    sorted_cubes = sorted(cubes, key=lambda x: (x[ax_equal[0]], x[ax_equal[1]], x[ax]))

    # Iterate over pairs of subseqent cubes and check if they are adjacent
    for i in range(1, n_cubes):
        cube_1 = sorted_cubes[i - 1]
        cube_2 = sorted_cubes[i]

        if (
            cube_1[ax_equal[0]] == cube_2[ax_equal[0]]
            and cube_1[ax_equal[1]] == cube_2[ax_equal[1]]
            and abs(cube_1[ax] - cube_2[ax]) == 1
        ):
            adjacent_count += 1

    return adjacent_count


def solution(cubes: Tuple[int]) -> int:
    n_cubes = len(cubes)
    n_connected_sides = (
        count_connected_sides(0, cubes, n_cubes)
        + count_connected_sides(1, cubes, n_cubes)
        + count_connected_sides(2, cubes, n_cubes)
    )

    surface_area = 6 * n_cubes - 2 * n_connected_sides
    return surface_area


if __name__ == "__main__":

    filepath = pathlib.Path("18/input.txt")
    cubes = get_cubes(filepath)

    print(solution(cubes))

    # Test 1
    filepath = pathlib.Path("18/input_test_1.txt")
    cubes_test = get_cubes(filepath)
    expected = 64
    assert solution(cubes_test) == expected

    # Test 2
    filepath = pathlib.Path("18/input_test_2.txt")
    cubes_test = get_cubes(filepath)
    expected = 30  # 6 connected sides -> 7 * 6 - 2*6
    assert solution(cubes_test) == expected

    # Test 3
    filepath = pathlib.Path("18/input_test_3.txt")
    cubes_test = get_cubes(filepath)
    expected = 36  # 6 connected sides -> 8 * 6 - 2*6
    assert solution(cubes_test) == expected

    # Test 4
    filepath = pathlib.Path("18/input_test_4.txt")
    cubes_test = get_cubes(filepath)
    expected = 32  # 8 connected sides -> 8 * 6 - 2*8
    assert solution(cubes_test) == expected

    # Test 5
    filepath = pathlib.Path("18/input_test_5.txt")
    cubes_test = get_cubes(filepath)
    expected = 36  # 9 connected sides -> 9 * 6 - 2*9
    assert solution(cubes_test) == expected

    # Test 6
    filepath = pathlib.Path("18/input_test_6.txt")
    cubes_test = get_cubes(filepath)
    expected = 36  # 12 connected sides -> 10 * 6 - 2*12
    assert solution(cubes_test) == expected
