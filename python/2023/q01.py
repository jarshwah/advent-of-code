import aocd

import utils


def part_one(raw: str) -> int:
    total = 0
    for line in utils.Input(raw).lines().strings:
        nums = []
        for c in line:
            if c.isdigit():
                nums.append(c)
        total += int(nums[0] + nums[-1])

    return total


def part_two(raw: str) -> int:
    words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    total = 0
    for line in utils.Input(raw).lines().strings:
        nums = []
        for idx, c in enumerate(line):
            if c.isdigit():
                nums.append(c)
            else:
                for num, word in enumerate(words, 1):
                    if line[idx : idx + len(word)].startswith(word):
                        nums.append(str(num))
                        break
        total += int(nums[0] + nums[-1])

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
