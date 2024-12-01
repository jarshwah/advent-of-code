import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str:
        return ""

    def part_two(self, input: utils.Input) -> str:
        return ""


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=2,
        test_answers=("", ""),
        test_input="""""",
    )
    runner.cli()
