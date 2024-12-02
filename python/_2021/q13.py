from functools import reduce

import aocd
from parse import parse

from utils import Point

Points = dict[Point, bool]


def parse_input(data: str) -> tuple[Points, list[Point]]:
    points: Points = {}
    folds: list[Point] = []
    for line in data.splitlines():
        if r := parse("fold along {}={:d}", line):
            folds.append((r[1], 0) if r[0] == "x" else (0, r[1]))
        elif (xy := line.split(",")) and xy[0]:
            points[tuple(map(int, xy))] = True
    return points, folds


def transpose(points: Points, fold: Point) -> Points:
    x, y = fold
    new_points: Points = {}
    # Can reduce to an unreadable dict-comp
    for px, py in points:
        nx = abs(x - abs(px - x))
        ny = abs(y - abs(py - y))
        new_points[nx, ny] = True
    return new_points


def part_one(data: str) -> int:
    points, folds = parse_input(data)
    new_points = transpose(points, folds[0])
    return len(new_points)


def part_two(data: str) -> None:
    points, folds = parse_input(data)
    points = reduce(transpose, folds, points)
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)
    for y in range(max_y + 1):
        print("".join(" #"[(x, y) in points] for x in range(max_x + 1)))


def test():
    test_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
    answer_1 = part_one(test_input)
    assert answer_1 == 17, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=13, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ")
    part_two(data)
