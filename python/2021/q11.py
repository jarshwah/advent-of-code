import math
import typing as t
from collections import deque

import aocd

from utils import Grid


def both_parts(grid: Grid) -> tuple[int, int]:
    flashes = 0
    a1 = 0
    for step in range(1, 500):
        queue = deque([])
        # increase energy
        for point, energy in grid.points.items():
            energy += 1
            grid.points[point] = energy
            if energy > 9:
                queue.append(point)

        # flash
        flashed = set()
        while queue:
            p = queue.popleft()
            if p in flashed:
                continue
            flashed.add(p)
            for neighbour in grid.get_neighbours(p, diag=True):
                grid.points[neighbour] += 1
                if grid.points[neighbour] > 9:
                    queue.append(neighbour)

        # reset
        for point in flashed:
            grid.points[point] = 0

        flashes += len(flashed)
        if step == 100:
            a1 = flashes
        if len(flashed) == len(grid.points):
            return a1, step


def test():
    test_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    grid = Grid(rows=((int(n) for n in row) for row in test_input.splitlines()))
    answer_1, answer_2 = both_parts(grid)
    assert answer_1 == 1656, answer_1
    assert answer_2 == 195, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=11, year=2021).splitlines()
    grid = Grid(rows=((int(n) for n in row) for row in data))
    a1, a2 = both_parts(grid)
    print("Part 1: ", a1)
    print("Part 2: ", a2)
