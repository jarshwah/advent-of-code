from functools import lru_cache

import typing as t
import aocd

from collections import Counter
from utils import int_numbers


def part_one(data: t.List[int]) -> int:
    data = sorted(data)
    # include outlet and device
    data = [0] + data + [data[-1] + 3]
    counter = Counter([jolt - data[i - 1] for i, jolt in enumerate(data)][1:])
    return counter[1] * counter[3]


def part_two(data: t.List[int]) -> int:
    data = sorted(data)
    valid = set(data)
    last = max(data)

    @lru_cache(maxsize=None)
    def combos(jolt):
        if jolt == last:
            return 1
        counter = 0
        for check in range(1, 4):
            if (check_jolt := jolt + check) in valid:
                counter += combos(check_jolt)
        return counter

    return combos(0)


if __name__ == "__main__":
    data = int_numbers(aocd.get_data(day=10, year=2020))
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
