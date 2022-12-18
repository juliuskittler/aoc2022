import pathlib
from typing import Tuple


def get_cubes(filepath: pathlib.Path) -> Tuple[int]:
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
        cubes = [tuple(map(int, line.split(","))) for line in lines]
        return cubes
