import dataclasses

import utils


@dataclasses.dataclass(order=True)
class Elf:
    total_calories: int = dataclasses.field(init=False)
    calories: list[int]

    def __post_init__(self):
        self.total_calories = sum(self.calories)


def parse(data: str) -> list[Elf]:
    return [Elf(calories=calories) for calories in utils.Input(data).group().integers]


class Puzzle(utils.Puzzle):
    def part_one_alt(self, input: utils.Input) -> str | int:
        """
        Find the sum of calories of the elf holding the most calories.
        """
        elves = parse(input.string)
        return sorted(elves, reverse=True)[0].total_calories

    def part_two_alt(self, input: utils.Input) -> str | int:
        """
        Find the sum of the caolories of the top 3 elves holding the most calories.
        """
        elves = parse(input.string)
        return sum(elf.total_calories for elf in sorted(elves, reverse=True)[:3])


puzzle = Puzzle(
    year=2022,
    day=1,
    test_answers=("24000", "45000"),
    test_input="""1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""",
)

if __name__ == "__main__":
    puzzle.cli()
