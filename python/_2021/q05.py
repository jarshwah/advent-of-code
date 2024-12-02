import itertools
import typing as t
from collections import Counter

import aocd

from utils import Point, line_algorithm


def parse(data: str) -> t.Iterable[tuple[Point, Point]]:
    for line in data.splitlines():
        L, R = line.split(" -> ")
        yield (tuple(map(int, L.split(","))), tuple(map(int, R.split(","))))


def part_one(data: str) -> int:
    # Horizontal / Vertical lines only
    points = [p for p in parse(data) if p[0][0] == p[1][0] or p[0][1] == p[1][1]]
    danger_zone = Counter(itertools.chain(*(line_algorithm(x, y) for x, y in points)))
    return len([k for k, v in danger_zone.items() if v >= 2])


def part_two(data: str) -> int:
    danger_zone = Counter(itertools.chain(*(line_algorithm(x, y) for x, y in parse(data))))
    return len([k for k, v in danger_zone.items() if v >= 2])


def test():
    test_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 5, answer_1
    assert answer_2 == 12, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=5, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
