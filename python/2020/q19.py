import typing as t

import aocd
import pyparsing as pp
import utils


def part_one(raw: str) -> int:
    rules, messages = utils.Input(raw).group().strings
    print(rules)
    print(messages)
    return 1


def part_two(raw: str) -> int:
    data = utils.Input(raw)
    return 1


def test():
    test_input = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 2, answer_1
    assert answer_2 == 1, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=19, year=2020)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
