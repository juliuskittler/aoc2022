import pathlib
from utils import get_coords
from typing import List, Tuple

"""
Note:
- First, identify the positions of all 
"""

def solution(row_idx: int, sensor_coords: List[Tuple], beacon_coords: List[Tuple]) -> int:
    pass


if __name__ == "__main__":

    filepath = pathlib.Path("15/input.txt")
    sensor_coords, beacon_coords = get_coords(filepath)
    row_idx = 2000000
    
    # print(solution(row_idx, sensor_coords, beacon_coords))

    # Test 1
    filepath = pathlib.Path("15/input_test_1.txt")
    sensor_coords_test, beacon_coords_test = get_coords(filepath)
    row_idx = 10
    expected = 26
    # assert(solution(row_idx, sensor_coords_test, beacon_coords_test)) == expected