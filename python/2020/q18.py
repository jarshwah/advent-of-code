from __future__ import annotations

import re
from dataclasses import dataclass

import aocd


@dataclass
class Basic:
    """
    All operators have the same precedence, so we change * to - which has
    equivalent precedence, but implement - as *.
    """

    val: int

    def __add__(self, other: Basic) -> Basic:
        return Basic(self.val + other.val)

    def __radd__(self, other: int):
        # work with sum
        return other + self.val

    def __sub__(self, other: Basic) -> Basic:
        return Basic(self.val * other.val)


@dataclass
class Advanced:
    """
    + has precedence over * so swap them around
    """

    val: int

    def __add__(self, other: Advanced) -> Advanced:
        return Advanced(self.val * other.val)

    def __radd__(self, other: int):
        # work with sum
        return other + self.val

    def __mul__(self, other: Advanced) -> Advanced:
        return Advanced(self.val + other.val)


def part_one(raw: str) -> int:
    expressions = raw.splitlines()
    return sum(
        eval(re.sub(r"\*", r"-", re.sub(r"(\d+)", r"Basic(\1)", expression)))
        for expression in expressions
    )


def part_two(raw: str) -> int:
    expressions = raw.splitlines()
    return sum(
        eval(
            re.sub(r"(\d+)", r"Advanced(\1)", expression)
            .replace("+", "x")
            .replace("*", "+")
            .replace("x", "*")
        )
        for expression in expressions
    )


def test():
    test_input = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 13632 + 12240, answer_1
    assert answer_2 == 23340 + 669060, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=18, year=2020)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
