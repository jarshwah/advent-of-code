import typing as t

import aocd
from parse import parse

from utils import Point

Points = dict[Point, bool]


def parse_input(data: str) -> tuple[Points, list[Point]]:
    points: Points = {}
    folds: list[Point] = []
    for line in data.splitlines():
        if r := parse("fold along {}={:d}", line):
            d, v = r[0], r[1]
            if d == "x":
                folds.append((v, 0))
            else:
                folds.append((0, v))

        elif r := parse("{:d},{:d}", line):
            p = (r[0], r[1])
            points[p] = True
    return points, folds


def transpose(points: Points, fold: Point) -> Points:
    x, y = fold
    if x > 0:
        return transpose_left(points, x)
    else:
        return transpose_up(points, y)


def transpose_left(points: Points, x: float) -> Points:
    new_points: Points = {}
    for px, py in points:
        if px < x:
            new_points[px, py] = True
        else:
            nx = 2 * x - px
            if nx >= 0:
                new_points[nx, py] = True
    return new_points


def transpose_up(points: Points, y: float) -> Points:
    new_points: Points = {}
    for px, py in points:
        if py < y:
            new_points[px, py] = True
        else:
            ny = 2 * y - py
            if ny >= 0:
                new_points[px, ny] = True
    return new_points


def part_one(data: str) -> int:
    points, folds = parse_input(data)
    fold = folds[0]
    new_points = transpose(points, fold)
    return sum(new_points.values())


def part_two(data: str) -> int:
    points, folds = parse_input(data)
    for fold in folds:
        print(f"{fold=}")
        points = transpose(points, fold)
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)
    for y in range(max_y + 1):
        print()
        for x in range(max_x + 1):
            char = "#" if (x, y) in points else "."
            print(char, end="")
    print()


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
    # answer_2 = part_two(test_input)
    assert answer_1 == 17, answer_1
    # assert answer_2 == 1, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=13, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ")
    part_two(data)
