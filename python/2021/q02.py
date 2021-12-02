import typing as t

import aocd
from parse import compile

import utils

parser = compile("{direction} {unit:d}")
DIRECTION = t.Literal["forward", "down", "up"]


def _produce(lines: list[str]) -> t.Iterator[tuple[DIRECTION, int]]:
    for line in lines:
        found = utils.only(parser.findall(line))
        yield found["direction"], found["unit"]


def part_one(data: list[str]) -> int:
    position = depth = 0
    for direction, units in _produce(data):
        if direction == "forward":
            position += units
        elif direction == "down":
            depth += units
        elif direction == "up":
            depth -= units
    return position * depth


def part_two(data: list[str]) -> int:
    position = depth = aim = 0
    for direction, units in _produce(data):
        if direction == "forward":
            position += units
            depth += units * aim
        elif direction == "down":
            aim += units
        elif direction == "up":
            aim -= units
    return position * depth


def test():
    test_input = """forward 5
down 5
forward 8
up 3
down 8
forward 2
"""
    answer_1 = part_one(test_input.splitlines())
    answer_2 = part_two(test_input.splitlines())
    assert answer_1 == 150, answer_1
    assert answer_2 == 900, answer_2


if __name__ == "__main__":
    test()

    data = aocd.get_data(day=2, year=2021).splitlines()
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
