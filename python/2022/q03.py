import string
import typing as t

import aocd
import utils

priority = f" {string.ascii_letters}"  # space at the front so that a is index 1


def part_one(raw: str) -> int:
    total = 0
    for rucksack in utils.Input(raw).split().strings:
        left, right = utils.partition_middle(rucksack)
        common = utils.only(set(left).intersection(set(right)))
        total += priority.index(common)
    return total


def part_two(raw: str) -> int:
    total = 0
    rucksacks = utils.Input(raw).split().strings
    for n in range(0, len(rucksacks), 3):
        sacks = [set(sack) for sack in rucksacks[n : n + 3]]
        common = utils.only(set.intersection(*sacks))
        total += priority.index(common)
    return total


def test():
    test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 157, answer_1
    assert answer_2 == 70, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=3, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
