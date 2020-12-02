import typing as t

import aocd


def parse(policy: str) -> t.Tuple[int, int, str, str]:
    count_range, letter, password = policy.split(" ")
    letter = letter.removesuffix(":")
    low, _, high = count_range.partition("-")
    return int(low), int(high), letter, password


def part_one(policies: t.List[str]) -> int:
    counter = 0
    for policy in policies:
        low, high, letter, password = parse(policy)
        if low <= password.count(letter) <= high:
            counter += 1
    return counter


def part_two(policies: t.List[str]) -> int:
    counter = 0
    for policy in policies:
        low, high, letter, password = parse(policy)
        if (password[low - 1] == letter) ^ (password[high - 1] == letter):
            counter += 1
    return counter


if __name__ == "__main__":
    policies = aocd.get_data(day=2, year=2020).splitlines()
    print("Part 1: ", part_one(policies))
    print("Part 2: ", part_two(policies))
