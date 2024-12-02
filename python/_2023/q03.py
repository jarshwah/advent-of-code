import re
from collections import defaultdict
from math import prod

import aocd

import utils


def part_one(raw: str) -> int:
    grid = utils.Input(raw).grid()
    total = 0
    ok_symbols = set(".0123456789")
    for rn, row in enumerate(grid.rows()):
        for match in re.finditer(r"(\d+)", "".join(row)):
            part_num = int(match.group(0))
            start = match.start()
            end = match.end()
            for cn in range(start, end):
                if any(
                    nb
                    for nb in grid.get_neighbours((rn, cn), diag=True)
                    if grid[nb] not in ok_symbols
                ):
                    total += part_num
                    break
    return total


def part_two(raw: str) -> int:
    grid = utils.Input(raw).grid()
    gears = defaultdict(set)
    GEAR = "*"
    for rn, row in enumerate(grid.rows()):
        for match in re.finditer(r"(\d+)", "".join(row)):
            part_num = int(match.group(0))
            start = match.start()
            end = match.end()
            for cn in range(start, end):
                for nb in (
                    nb for nb in grid.get_neighbours((rn, cn), diag=True) if grid[nb] == GEAR
                ):
                    gears[nb].add(part_num)
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
