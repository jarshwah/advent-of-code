import itertools
import typing as t
import aocd


def part_one(data: t.List[int]) -> int:
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
