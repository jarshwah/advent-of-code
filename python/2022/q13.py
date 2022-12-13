import itertools
from ast import literal_eval
from functools import cmp_to_key
from typing import Literal, Type

import aocd
import utils

RecursiveInt = int | None | list["RecursiveInt"]


def compare_recursive(left: RecursiveInt, right: RecursiveInt) -> int:
    if left is None:
        return -1
    if right is None:
        return 1
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        return 0

    if isinstance(left, list) and isinstance(right, list):
        if not left:
            return -1
        if not right:
            return 1
        for pair in itertools.zip_longest(left, right, fillvalue=None):
            compared = compare_recursive(pair[0], pair[1])
            if compared == 0:
                continue
            return compared
        return 0
    if isinstance(left, int):
        return compare_recursive([left], right)
    if isinstance(right, int):
        return compare_recursive(left, [right])
    raise ValueError(left, right)


def part_one(raw: str) -> int:
    ordered = []
    for pair_num, pair in enumerate(utils.Input(raw).group("\n\n", sep="\n").strings, 1):
        left = literal_eval(pair[0])
        right = literal_eval(pair[1])
        if compare_recursive(left, right) < 0:
            ordered.append(pair_num)
    return sum(ordered)


def part_two(raw: str) -> int:
    packets = []
    for pair in utils.Input(raw).group("\n\n", sep="\n").strings:
        packets.extend([literal_eval(pair[0]), literal_eval(pair[1])])
    packets.extend(([[2]], [[6]]))
    sorted_packets = sorted(packets, key=cmp_to_key(compare_recursive))

    return (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)


def test():
    test_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 13, answer_1
    assert answer_2 == 140, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=13, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
