import aocd

import utils


def how_many_after(fish: list[int], days: int) -> int:
    # days -> num fish
    timers = {n: 0 for n in range(9)}
    for f in fish:
        timers[f] += 1
    for _ in range(days):
        spawning = timers[0]
        for day in range(1, 9):
            timers[day - 1] = timers[day]
        timers[6] += spawning
        timers[8] = spawning
    return sum(timers.values())


def part_one(numbers: list[int]) -> int:
    how_many_after(numbers, 80)


def part_two(numbers: list[int]) -> int:
    return how_many_after(numbers, 256)


def test():
    test_input = [3, 4, 3, 1, 2]
    answer_1 = how_many_after(test_input, 80)
    answer_2 = how_many_after(test_input, 256)
    assert answer_1 == 5934, answer_1
    assert answer_2 == 26984457539, answer_2


if __name__ == "__main__":
    test()
    numbers = utils.int_numbers(aocd.get_data(day=6, year=2021), sep=",")
    print("Part 1: ", part_one(numbers))
    print("Part 2: ", part_two(numbers))
