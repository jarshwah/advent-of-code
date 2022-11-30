import typing as t

import aocd
import utils


def part_one(data: str) -> int:
    return 1


def part_two(data: str) -> int:
    return 1


def test():
    test_input = []
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 1, answer_1
    assert answer_2 == 1, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=1, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
