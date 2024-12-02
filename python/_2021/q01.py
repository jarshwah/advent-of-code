import aocd

import utils


def part_one(numbers: list[int]) -> int:
    """
    Find the count of increasing depth given a list of depths
    """
    return sum(pair[1] > pair[0] for pair in zip(numbers, numbers[1:]))


def part_two(numbers: list[int]) -> int:
    """
    Find the count of increasing depth for a 3 dimensional sliding window of depth sums
    """
    windows = list(zip(numbers, numbers[1:], numbers[2:]))
    return sum(sum(pair[1]) > sum(pair[0]) for pair in zip(windows, windows[1:]))


def test():
    numbers = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263,
    ]
    answer_1 = part_one(numbers)
    answer_2 = part_two(numbers)
    assert answer_1 == 7, answer_1
    assert answer_2 == 5, answer_2


if __name__ == "__main__":
    test()
    numbers = utils.int_numbers(aocd.get_data(day=1, year=2021))
    print(part_one(numbers))
    print(part_two(numbers))
