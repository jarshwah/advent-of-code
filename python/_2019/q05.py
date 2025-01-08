import intcode

import utils


class Puzzle(utils.Puzzle):
    """--- Day 5: Sunny with a Chance of Asteroids ---"""

    def part_one(self, input: utils.Input) -> str | int:
        program = intcode.IntCode(input.split(",").numbers, input=[1])
        program.run()
        return int(program.output[-1])

    def part_two(self, input: utils.Input) -> str | int:
        program = intcode.IntCode(input.split(",").numbers, input=[5])
        program.run()
        return int(program.output[-1])


if __name__ == "__main__":
    runner = Puzzle(year=2019, day=5, no_tests=True)
    runner.cli()
