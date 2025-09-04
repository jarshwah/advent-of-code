import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Find the sum of calories of the elf holding the most calories.
        """
        return max(sum(group) for group in input.group().integers)

    def part_two(self, input: utils.Input) -> str | int:
        """
        Find the sum of the caolories of the top 3 elves holding the most calories.
        """
        return sum(sorted(sum(group) for group in input.group().integers)[-3:])


puzzle = Puzzle(
    year=2022,
    day=1,
    test_answers=("24000", "45000"),
    test_input="""\
1000
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
