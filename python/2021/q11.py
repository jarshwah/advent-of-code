from collections import deque
from typing import Deque

import aocd

from utils import Grid, Point


def both_parts(grid: Grid) -> tuple[int, int]:
    flashes = 0
    a1 = 0
    queue: Deque[Point] = deque([])

    def _inc(p):
        grid[p] += 1
        if grid[p] > 9:
            queue.append(p)

    for step in range(1, 500):
        for point in grid:
            _inc(point)

        flashed = set()
        while queue:
            p = queue.popleft()
            if p in flashed:
                continue
            flashed.add(p)
            for neighbour in grid.get_neighbours(p, diag=True):
                _inc(neighbour)

        for point in flashed:
            grid[point] = 0

        flashes += len(flashed)
        if step == 100:
            a1 = flashes
        if len(flashed) == len(grid):
            return a1, step
    return -1, -1


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
