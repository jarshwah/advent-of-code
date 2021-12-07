from bisect import bisect_left
from math import factorial
from statistics import mean, median

import aocd

import utils


def compute_changes(depths: list[int], target: int) -> int:
    return sum(int(abs(depth - target)) for depth in depths)


def compute_changes_scaled(depths: list[int], target: int) -> int:
    return sum(sum(range(1, int(abs(depth - target) + 1))) for depth in depths)


def part_one(numbers: list[int]) -> int:
    depths = sorted(numbers)
    partition = depths
    target = int(median(depths))
    optimal = compute_changes(depths, target)
    while len(partition) > 1:
        target = int(median(partition))
        changes = compute_changes(depths, target)
        optimal = min(optimal, changes)
        l, r = utils.split_list(partition)
        lc = compute_changes(depths, median(l))
        rc = compute_changes(depths, median(r))
        if lc <= rc:
            partition = l
        else:
            partition = r
    return optimal


def part_two(numbers: list[int]) -> int:
    depths = sorted(numbers)
    target = mean(depths)
    low, high = int(target), int(target + 1)
    lc = compute_changes_scaled(depths, low)
    rc = compute_changes_scaled(depths, high)
    return min(lc, rc)


def test():
    test_input = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 37, answer_1
    assert answer_2 == 168, answer_2


if __name__ == "__main__":
    test()
    numbers = utils.int_numbers(aocd.get_data(day=7, year=2021), sep=",")
    print("Part 1: ", part_one(numbers))
    print("Part 2: ", part_two(numbers))
