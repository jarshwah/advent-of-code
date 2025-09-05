import enum
from ast import literal_eval
import more_itertools
import utils


def parse(raw: str) -> dict[str, M]:
    cave: dict[utils.Point, M] = {}
    for path in raw.splitlines():
        paths = [tuple(reversed(literal_eval(point.strip()))) for point in path.split(" -> ")]
        for from_point, to_point in more_itertools.pairwise(paths):
            for rock in utils.line_algorithm(from_point, to_point):
                cave[rock] = M.ROCK
    return cave


def part_two_alt(raw: str) -> int:
    """
    Does not work yet.

    Compute the 2-triangle number from the origin to the floor which gives us
    the full possible triange.

    Then remove the total count of rocks.

    Then remove the 2-triange count from beneath each horizontal line of rocks,
    since no sand can flow there (excluding spaces occupied by rocks).

    Issues:
        1. Rocks like ###.###.### should count as an uninterupted line where
           the gaps would have been excluded by a previous triangle

        2. Need to account for where a full side of a triangle is blocked by a
           vertical wall (it cuts the triangle and stops sand getting in, expanding
           the empty space within)
    """
    floor = 0
    rocks = set()
    empty = set()
    horizontal_lines = []
    for path in raw.splitlines():
        paths = [tuple(reversed(literal_eval(point.strip()))) for point in path.split(" -> ")]
        for from_point, to_point in more_itertools.pairwise(paths):
            for rock in utils.line_algorithm(from_point, to_point):
                rocks.add(rock)
            floor = max(floor, to_point[0])
            if from_point[0] == to_point[0]:
                # capture horizontal lines so we can exclude the triangle beneath them
                horizontal_lines.append((from_point, to_point))
    floor += 2

    # Remove the triangular space beneath each horizontal line
    for from_point, to_point in horizontal_lines:
        rnum = from_point[0]
        cmin, cmax = sorted((from_point[1], to_point[1]))
        rows = (cmax - cmin) // 2
        for rdiff in range(1, rows + 1):
            if rnum + rdiff >= floor:
                break
            for cdiff in range(cmin + rdiff, cmax - rdiff + 1):
                excluded = (rnum + rdiff, cdiff)
                empty.add(excluded)
                # TODO: if we run into a rock on the right we have to stop
                # TODO: if we run into a rock on the left, we shouldn't reduce the left
                # TODO: empty triangles act as rocks when computing space beneath ie ###.### should be continuous
    sand_can_occupy = floor**2
    return sand_can_occupy - len(rocks | empty)


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
            if p == (0, 500):
                print("+", end="")
            elif p in cave:
                print(cave[p].value, end="")
            else:
                print(M.AIR.value, end="")


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
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

    def part_two(self, input: utils.Input) -> str | int:
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


puzzle = Puzzle(
    year=2022,
    day=14,
    test_answers=("24", "93"),
    test_input="""\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""",
)

if __name__ == "__main__":
    puzzle.cli()
