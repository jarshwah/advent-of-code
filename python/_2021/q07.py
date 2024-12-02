from statistics import mean, median

import aocd

import utils


def part_one(numbers: list[int]) -> int:
    return sum(abs(depth - int(median(numbers))) for depth in numbers)


def compute_changes_scaled(depths: list[int], target: int) -> int:
    return sum(utils.triangle_number(abs(target - depth)) for depth in depths)


def part_two(numbers: list[int]) -> int:
    target = int(mean(numbers))
    # either integer surrounding the float
    lc = compute_changes_scaled(numbers, target)
    rc = compute_changes_scaled(numbers, target + 1)
    return min(lc, rc)


def test():
    test_input = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 37, answer_1
    assert answer_2 == 168, answer_2


if __name__ == "__main__":
    test()
    numbers = sorted(utils.int_numbers(aocd.get_data(day=7, year=2021), sep=","))
    print("Part 1: ", part_one(numbers))
    print("Part 2: ", part_two(numbers))
