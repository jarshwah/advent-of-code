from collections import deque
import itertools
import typing as t
import aocd


def part_one_optimised(data: t.List[int]) -> int:
    """
    I expected that this version would have better performance as it doesn't
    need to re-compute the combinations of all "middle" numbers. Turns out that
    computing every combination, once, is more expensive than recomputing a subset
    of combinations many times.

    Runtime: 29.6ms
    """
    low = 0
    high = 25
    queue = [sum(pair) for pair in itertools.combinations(data[low:high], 2)]
    while high < len(data):
        check = data[high]
        if check not in queue:
            return check
        queue = queue[low % 25 :]
        low += 1
        high += 1
        for item in data[low:high]:
            queue.append(item + check)
    return -1


def part_one(data: t.List[int]) -> int:
    """5.75ms"""
    low = 0
    high = 25
    while high < len(data):
        check = data[high]
        if not any(
            True for pair in itertools.combinations(data[low:high], 2) if sum(pair) == check
        ):
            return check
        low += 1
        high += 1
    return -1


def part_two(data: t.List[int], target: int) -> int:
    if target <= 0:
        return -1
    start = end = 0
    while end < len(data):
        sum_range = sum(data[start:end])
        if sum_range == target:
            return min(data[start:end]) + max(data[start:end])
        elif sum_range < target:
            end += 1
        elif sum_range > target:
            start += 1
    return -1


if __name__ == "__main__":
    data = [int(num) for num in aocd.get_data(day=9, year=2020).splitlines()]
    p1 = part_one(data)
    print("Part 1: ", p1)
    print("Part 2: ", part_two(data, p1))
