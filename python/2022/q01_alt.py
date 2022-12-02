import dataclasses

import aocd
import utils


@dataclasses.dataclass(order=True)
class Elf:
    total_calories: int = dataclasses.field(init=False)
    calories: list[int]

    def __post_init__(self):
        self.total_calories = sum(self.calories)


def part_one(elves: list[Elf]) -> int:
    """
    Find the sum of calories of the elf holding the most calories.
    """
    return sorted(elves, reverse=True)[0].total_calories


def part_two(elves: list[Elf]) -> int:
    """
    Find the sum of the caolories of the top 3 elves holding the most calories.
    """
    return sum(elf.total_calories for elf in sorted(elves, reverse=True)[:3])


def test():
    data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
    elves = parse(data)
    answer_1 = part_one(elves)
    answer_2 = part_two(elves)
    assert answer_1 == 24000, answer_1
    assert answer_2 == 45000, answer_2


def parse(data: str) -> list[Elf]:
    return [Elf(calories=calories) for calories in utils.Input(data).group().integers]


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=1, year=2022)
    elves = parse(data)
    print("Part 1: ", part_one(elves))
    print("Part 2: ", part_two(elves))
