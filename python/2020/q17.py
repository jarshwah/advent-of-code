import itertools
from collections import deque
from typing import Callable

import aocd
from utils import Point3d, Point4d, PointNd


def neighbours_3d(point: Point3d) -> list[Point3d]:
    return [
        (point[0] + nb[0], point[1] + nb[1], point[2] + nb[2])
        for nb in itertools.product(*itertools.repeat([-1, 0, 1], 3))
        if nb != (0, 0, 0)
    ]


def neighbours_4d(point: Point4d) -> list[Point4d]:
    return [
        (point[0] + nb[0], point[1] + nb[1], point[2] + nb[2], point[3] + nb[3])
        for nb in itertools.product(*itertools.repeat([-1, 0, 1], 4))
        if nb != (0, 0, 0, 0)
    ]


def solve(grid: PointNd, neighbours: Callable[[PointNd], PointNd]) -> int:
    for _ in range(6):
        new = grid.copy()
        cubes = deque(grid.keys())
        done = set()
        while cubes:
            cube = cubes.pop()
            if cube in done:
                continue
            done.add(cube)

            all_neighbours = neighbours(cube)
            outside = [nb for nb in all_neighbours if nb not in grid and nb not in done]
            active_neighbours = sum(grid.get(nb, False) for nb in all_neighbours)
            if grid.get(cube, False):
                # We add all outside neighbours to be checked if we have an active cube
                cubes.extend(outside)
                new[cube] = 2 <= active_neighbours <= 3
            elif active_neighbours == 3:
                new[cube] = True
            else:
                new[cube] = False

        grid = new
    return sum(grid.values())


def part_one(raw: str) -> int:
    grid = {}
    for rn, line in enumerate(raw.splitlines()):
        for cn, node in enumerate(line):
            grid[rn, cn, 0] = node == "#"
    return solve(grid, neighbours_3d)


def part_two(raw: str) -> int:
    grid = {}
    for rn, line in enumerate(raw.splitlines()):
        for cn, node in enumerate(line):
            grid[rn, cn, 0, 0] = node == "#"
    return solve(grid, neighbours_4d)


def test():
    test_input = """.#.
..#
###"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 112, answer_1
    assert answer_2 == 848, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=17, year=2020)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
