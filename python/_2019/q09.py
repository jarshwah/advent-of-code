import intcode

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        program = input.split(",").numbers
        interpreter = intcode.IntCode(program)
        interpreter.input.write(1)  # test mode
        return int(interpreter.run()[-1])

    def part_two(self, input: utils.Input) -> str | int:
        program = input.split(",").numbers
        interpreter = intcode.IntCode(program)
        interpreter.input.write(2)
        return int(interpreter.run()[-1])


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=9,
        test_answers=("99", "99"),
        test_input="""109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99""",
    )
    runner.cli()
