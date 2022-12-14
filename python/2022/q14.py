import copy
import enum
from ast import literal_eval

import aocd
import more_itertools
import utils


class M(str, enum.Enum):
    AIR = "."
    ROCK = "#"
    SAND = "O"


def parse(raw: str) -> dict[str, M]:
    cave: dict[utils.Point, M] = {}
    for path in raw.splitlines():
        paths = [tuple(reversed(literal_eval(point.strip()))) for point in path.split(" -> ")]
        for from_point, to_point in more_itertools.pairwise(paths):
            for rock in utils.line_algorithm(from_point, to_point):
                cave[rock] = M.ROCK
    return cave


def part_one(cave: dict[str, M]) -> int:
    origin = (0, 500)
    floor = max(k[0] for k in cave)
    grains = 0
    grain = origin
    while grain[0] < floor:
        grain = origin
        while grain[0] < floor:
            for direction in (utils.DOWN, utils.DOWNLEFT, utils.DOWNRIGHT):
                check = utils.sum_points(grain, direction)
                if check not in cave:
                    grain = check
                    break
            else:
                cave[grain] = M.SAND
                grains += 1
                break
    return grains


def part_two(cave: dict[str, M]) -> int:
    origin = (0, 500)
    floor = max(k[0] for k in cave) + 2
    grains = 0
    grain = origin
    cave[origin] = M.AIR
    while cave[origin] != M.SAND:
        grain = origin
        while grain[0] < floor:
            for direction in (utils.DOWN, utils.DOWNLEFT, utils.DOWNRIGHT):
                check = utils.sum_points(grain, direction)
                if check not in cave:
                    grain = check
                    break
            else:
                cave[grain] = M.SAND
                grains += 1
                break
        else:
            cave[grain] = M.SAND
    return grains


def print_cave(cave: dict[utils.Point, M]) -> None:
    print()
    rmin = min(k[0] for k in cave)
    rmax = max(k[0] for k in cave)
    cmin = min(k[1] for k in cave)
    cmax = max(k[1] for k in cave)
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
    cave = parse(test_input)
    answer_1 = part_one(copy.deepcopy(cave))
    answer_2 = part_two(cave)
    assert answer_1 == 24, answer_1
    assert answer_2 == 93, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=14, year=2022)
    cave = parse(data)
    print("Part 1: ", part_one(copy.deepcopy(cave)))
    print("Part 2: ", part_two(cave))
