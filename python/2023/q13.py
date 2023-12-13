from operator import itemgetter
from typing import Literal

import aocd

import utils

ORIENTATION = Literal["|", "-"]
COL = "|"
ROW = "-"


def reflects(
    grid: utils.Grid,
    start: utils.Point,
    end: utils.Point,
    start_direction: utils.Point,
    end_direction: utils.Point,
) -> bool:
    while True:
        if start not in grid or end not in grid:
            return True
        if grid[start] != grid[end]:
            return False
        start = utils.sum_points(start, start_direction)
        end = utils.sum_points(end, end_direction)


def find_reflection_point(grid: utils.Grid, counter: int) -> tuple[ORIENTATION, utils.Point]:
    # Start from the middle and work outwards
    start_rc = round(grid.height / 2)
    start_cc = round(grid.width / 2)

    queue = [
        (utils.Point((start_rc, start_cc)), "|"),
        (utils.Point((start_rc, start_cc)), "-"),
    ]
    rows = []

    for r in range(1, start_rc + 1):
        # move up and down
        rows.append((utils.Point((start_rc + r, start_cc)), ROW))
        rows.append((utils.Point((start_rc - r, start_cc)), ROW))
    cols = []

    for c in range(1, start_cc + 1):
        # move left and right
        cols.append((utils.Point((start_rc, start_cc + c)), COL))
        cols.append((utils.Point((start_rc, start_cc - c)), COL))

    # Order by inside out
    for row, col in zip(rows, cols):
        queue.extend([row, col])

    for point, orientation in queue:
        if point not in grid:
            continue
        if orientation == ROW:
            go_down = utils.sum_points(point, utils.DOWN)
            go_up = utils.sum_points(point, utils.UP)
            if reflects(grid, point, go_down, utils.UP, utils.DOWN):
                return orientation, min(point, go_down, key=itemgetter(0))
            if reflects(grid, point, go_up, utils.DOWN, utils.UP):
                return orientation, min(point, go_up, key=itemgetter(0))
        if orientation == COL:
            go_right = utils.sum_points(point, utils.RIGHT)
            go_left = utils.sum_points(point, utils.LEFT)
            if reflects(grid, point, go_right, utils.LEFT, utils.RIGHT):
                return orientation, min(point, go_right, key=itemgetter(1))
            if reflects(grid, point, go_left, utils.RIGHT, utils.LEFT):
                return orientation, min(point, go_left, key=itemgetter(1))
    raise ValueError("No reflection point found")


def part_one_orig(raw: str) -> int:
    valleys = utils.Input(raw).group("\n\n", sep="\n").strings
    reflections = []
    for vn, valley in enumerate(valleys, 1):
        grid = utils.Grid(valley)
        reflections.append(find_reflection_point(grid, vn))
    total = 0

    for orientation, point in reflections:
        if orientation == ROW:
            total += 100 * (point[0] + 1)
        else:
            total += point[1] + 1
    return total


def index_of_reflection(lines: list[int], diffs_allowed: int = 0) -> int:
    diffs = 0
    for idx, (start, compare) in enumerate(zip(lines, lines[1:])):
        if start == compare:
            for offset in range(1, len(lines) - idx):
                sidx = idx - offset
                eidx = idx + 1 + offset
                if sidx < 0 or eidx >= len(lines):
                    return idx if diffs == diffs_allowed else -1
                if lines[sidx] != lines[eidx]:
                    break
    return -1


def reflections(lines: list[str], diffs_allowed: int = 0) -> int:
    line_count = 0
    for pos in range(len(lines) - 1):
        diffs = 0
        for start, compare in zip(lines[pos + 1 :], lines[pos::-1]):
            diffs += sum(1 if sx != cx else 0 for sx, cx in zip(start, compare))
        if diffs == diffs_allowed:
            line_count += pos + 1
    return line_count


def index_of_reflection_diffs(lines: list[int], diffs_allowed: int = 0) -> int:
    diffs = 0
    for idx, (start, compare) in enumerate(zip(lines, lines[1:])):
        diff_by_one = one_bit_diff(start, compare)
        if start == compare or diff_by_one:
            if diff_by_one:
                diffs += 1
            for offset in range(1, len(lines) - idx):
                sidx = idx - offset
                eidx = idx + 1 + offset
                if sidx < 0 or eidx >= len(lines):
                    if diffs == diffs_allowed:
                        return idx
                    # diffs = 0
                    continue
                if lines[sidx] != lines[eidx]:
                    if one_bit_diff(lines[sidx], lines[eidx]):
                        diffs += 1
                    if diffs > diffs_allowed:
                        break
    return -1


def one_bit_diff(left: int, right: int) -> bool:
    if diff := left ^ right:
        return not (diff & (diff - 1))
    return False


def part_one(raw: str) -> int:
    valleys = utils.Input(raw.replace("#", "1").replace(".", "0")).group("\n\n", sep="\n").strings
    total = 0
    for valley in valleys:
        row_wise = [int(row, 2) for row in valley]
        if (idx := index_of_reflection(row_wise)) != -1:
            total += (idx + 1) * 100
            continue
        else:
            col_wise = [int("".join(col), 2) for col in utils.transpose(valley)]
            idx = index_of_reflection(col_wise) + 1
            total += idx
    return total


def part_two(raw: str) -> int:
    valleys = utils.Input(raw).group("\n\n", sep="\n").strings
    total = 0
    for vn, valley in enumerate(valleys):
        row_wise = [row for row in valley]
        col_wise = [col for col in utils.transpose(valley)]
        total += reflections(row_wise, diffs_allowed=1) * 100
        total += reflections(col_wise, diffs_allowed=1)
    return total


def test():
    test_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 405, answer_1
    assert answer_2 == 400, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=13, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
