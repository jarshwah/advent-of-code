import re
import aocd
import utils


def part_one(raw: str) -> int:
    total = 0
    for line in utils.Input(raw).lines().strings:
        nums = []
        for c in line:
            if c.isdigit():
                nums.append(c)
        total += int(f"{nums[0]}{nums[-1]}")

    return total


def part_two(raw: str) -> int:
    total = 0
    for line in utils.Input(raw).lines().strings:
        line = re.sub("one", "o1e", line)
        line = re.sub("two", "t2o", line)
        line = re.sub("three", "t3e", line)
        line = re.sub("four", "f4r", line)
        line = re.sub("five", "f5e", line)
        line = re.sub("six", "s6x", line)
        line = re.sub("seven", "s7n", line)
        line = re.sub("eight", "e8t", line)
        line = re.sub("nine", "n9e", line)

        nums = []
        for c in line:
            if c.isdigit():
                nums.append(c)
        total += int(f"{nums[0]}{nums[-1]}")

    return total


def test():
    answer_1 = part_one(
        """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
    )
    answer_2 = part_two(
        """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    )
    assert answer_1 == 142, answer_1
    assert answer_2 == 281, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=1, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
