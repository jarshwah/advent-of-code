from math import prod
from collections import defaultdict
import copy
import aocd
import utils
import re


def part_one(raw: str) -> int:
    data = utils.Input(raw).lines().strings
    config = {"red": 12, "green": 13, "blue": 14}
    valid = 0
    pattern = r"(\d+) (\w+)"
    for line in data:
        game_number = int(line.split(":")[0][4:])
        too_many = False
        for sets in line.split(":")[1].split(";"):
            ours = copy.copy(config)
            for match in re.findall(pattern, sets):
                ours[match[1]] -= int(match[0])
            if any(v < 0 for v in ours.values()):
                too_many = True
                break
        if not too_many:
            valid += game_number
            continue
    return valid


def part_two(raw: str) -> int:
    data = utils.Input(raw).lines().strings
    total = 0
    pattern = r"(\d+) (\w+)"
    for line in data:
        counts = defaultdict(list)
        for sets in line.split(":")[1].split(";"):
            for match in re.findall(pattern, sets):
                counts[match[1]].append(int(match[0]))
        power = prod([max(nums) for nums in counts.values()])
        total += power
    return total


def test():
    test_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 8, answer_1
    assert answer_2 == 2286, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=2, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
