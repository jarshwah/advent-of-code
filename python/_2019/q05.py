import intcode

import utils


class Puzzle(utils.Puzzle):
    """--- Day 5: Sunny with a Chance of Asteroids ---"""

    def part_one(self, input: utils.Input) -> str | int:
        program = intcode.IntCode(input.split(",").numbers)
        program.input.write(1)
        return int(program.run()[-1])

    def part_two(self, input: utils.Input) -> str | int:
        program = intcode.IntCode(input.split(",").numbers)
        program.input.write(5)
        return int(program.run()[-1])


puzzle = Puzzle(year=2019, day=5, no_tests=True)

if __name__ == "__main__":
    puzzle.cli()
