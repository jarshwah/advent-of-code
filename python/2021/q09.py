import math
import typing as t

import aocd

from utils import Grid


def mindepth(check, neighbours) -> bool:
    return all(check[1] < nv[1] for nv in neighbours)


def notnine(check, neighbours) -> bool:
    return check[1] < 9


def part_one(grid: Grid) -> int:
    return sum(val + 1 for _, val in grid.search(mindepth))


def part_two(grid: Grid) -> int:
    low_points = [p for p, v in grid.search(mindepth)]
    sizes = []
    for lp in low_points:
        matches = list(grid.collect_recursive([lp], notnine))
        sizes.append(len(matches))
    top3 = sorted(sizes, reverse=True)[:3]
    return math.prod(top3)


def test():
    test_input = """2199943210
3987894921
9856789892
8767896789
9899965678"""
    grid = Grid(rows=((int(n) for n in row) for row in test_input.splitlines()))
    answer_1 = part_one(grid)
    answer_2 = part_two(grid)
    assert answer_1 == 15, answer_1
    assert answer_2 == 1134, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=9, year=2021).splitlines()
    grid = Grid(rows=((int(n) for n in row) for row in data))
    print("Part 1: ", part_one(grid))
    print("Part 2: ", part_two(grid))
