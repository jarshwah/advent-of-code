import enum
import typing as t
from ast import literal_eval
from collections import defaultdict

import aocd
import more_itertools
import utils


class M(str, enum.Enum):
    AIR = "."
    ROCK = "#"
    SAND = "O"


def part_one(raw: str) -> int:
    origin = (0, 500)
    floor = 0
    cave: dict[utils.Point, M] = {}
    for path in raw.splitlines():
        paths = [tuple(reversed(literal_eval(point.strip()))) for point in path.split(" -> ")]
        for from_point, to_point in more_itertools.pairwise(paths):
            for rock in utils.line_algorithm(from_point, to_point):
                cave[rock] = M.ROCK
                floor = max(floor, rock[0])

    grains = 0
    grain = origin
    while grain[0] < floor:
        grains += 1
        grain = origin
        while grain[0] < floor:
            directions = [
                utils.sum_points(grain, utils.DOWN),
                utils.sum_points(grain, utils.DOWNLEFT),
                utils.sum_points(grain, utils.DOWNRIGHT),
            ]
            for direction in directions:
                if direction not in cave:
                    grain = direction
                    break
            else:
                cave[grain] = M.SAND
                break
    return grains - 1


def part_two(raw: str) -> int:
    origin = (0, 500)
    floor = 0
    cave: dict[utils.Point, str] = {}
    for path in raw.splitlines():
        paths = [tuple(reversed(literal_eval(point.strip()))) for point in path.split(" -> ")]
        for from_point, to_point in more_itertools.pairwise(paths):
            for rock in utils.line_algorithm(from_point, to_point):
                cave[rock] = M.ROCK
                floor = max(floor, rock[0])

    grains = 0
    grain = origin
    floor += 2
    cave[origin] = M.AIR
    while cave[origin] != M.SAND:
        grain = origin
        while cave[origin] != M.SAND and grain[0] < floor:
            directions = [
                utils.sum_points(grain, utils.DOWN),
                utils.sum_points(grain, utils.DOWNLEFT),
                utils.sum_points(grain, utils.DOWNRIGHT),
            ]
            for direction in directions:
                if direction not in cave:
                    grain = direction
                    break
            else:
                cave[grain] = M.SAND
                grains += 1
                # print_cave(cave)
                break
        else:
            cave[grain] = M.SAND
    return grains


def print_cave(cave: dict[utils.Point, M]) -> None:
    print()
    rmin = min([k[0] for k in cave])
    rmax = max([k[0] for k in cave])
    cmin = min([k[1] for k in cave])
    cmax = max([k[1] for k in cave])
    for r in range(rmin, rmax):
        print("\n", end="")
        for c in range(cmin, cmax):
            p = (r, c)
            if p in cave:
                print(cave[p].value, end="")
            else:
                print(M.AIR.value, end="")


def test():
    test_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
    # answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    # assert answer_1 == 24, answer_1
    assert answer_2 == 93, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=14, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
