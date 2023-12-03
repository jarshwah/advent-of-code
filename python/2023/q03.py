import re
from collections import defaultdict
from math import prod

import aocd

import utils

ok_symbols = set(".0123456789")


class Found(Exception):
    pass


def part_one(raw: str) -> int:
    parts = []
    grid = []
    for row in utils.Input(raw).lines().strings:
        grid.append(row)

    rc = len(grid)
    cc = len(grid[0])

    for rn, row in enumerate(grid):
        line = "".join(row)
        for match in re.finditer(r"(\d+)", line):
            part_num = match.group(0)
            start = match.start()
            end = match.end()
            try:
                for cn in range(start, end):
                    if any(
                        grid[nr][nc] not in ok_symbols
                        for nr, nc in utils.neighbours((rn, cn), utils.DIRECTIONS_8)
                        if 0 <= nr < rc and 0 <= nc < cc
                    ):
                        raise Found
            except Found:
                parts.append(int(part_num))
    return sum(parts)


def part_two(raw: str) -> int:
    grid = []
    for row in utils.Input(raw).lines().strings:
        grid.append(row)

    rc = len(grid)
    cc = len(grid[0])
    gears = defaultdict(list)
    for rn, row in enumerate(grid):
        line = "".join(row)
        for match in re.finditer(r"(\d+)", line):
            part_num = int(match.group(0))
            start = match.start()
            end = match.end()
            try:
                for cn in range(start, end):
                    for nr, nc in utils.neighbours((rn, cn), utils.DIRECTIONS_8):
                        if 0 <= nr < rc and 0 <= nc < cc:
                            if grid[nr][nc] == "*":
                                gears[(nr, nc)].append(part_num)
                                raise Found
            except Found:
                pass
    return sum(prod(nums) for nums in gears.values() if len(nums) == 2)


def test():
    test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 4361, answer_1
    assert answer_2 == 467835, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=3, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
