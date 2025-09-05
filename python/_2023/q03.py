import re
from collections import defaultdict
from math import prod
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid()
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

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.grid()
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


puzzle = Puzzle(
    year=2023,
    day=3,
    test_answers=("4361", "467835"),
    test_input="""\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""",
)

if __name__ == "__main__":
    puzzle.cli()
