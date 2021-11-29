import itertools
import math
import typing as t

import aocd

import utils


def part_one(numbers: t.List[int]):
    """
    Find the two numbers that sum to 2020 and multiply them for the answer

    O(n log n)
    """
    numbers.sort()
    start = 0
    end = len(numbers) - 1
    while start < end:
        first, second = numbers[start], numbers[end]
        result = first + second
        if result < 2020:
            start += 1
        elif result > 2020:
            end -= 1
        else:
            print(f"Part 1: {first} * {second} = {first * second}")
            return
    print("No Solution")


def part_two(numbers: t.List[int]):
    """
    Find the three numbers that sum to 2020 and multiply them for the answer

    O(n^3)
    """
    for combo in itertools.combinations(numbers, 3):
        if sum(combo) == 2020:
            print(f"Part 2: {' * '.join(map(str, combo))} = {math.prod(combo)}")
            return
    print("No Solution")


if __name__ == "__main__":
    numbers = utils.int_numbers(aocd.get_data(day=1, year=2020))
    part_one(numbers)
    part_two(numbers)
