from contextlib import suppress

import intcode

import utils


class Puzzle(utils.Puzzle):
    """--- Day 2: 1202 Program Alarm ---"""

    def part_one(self, input: utils.Input) -> str | int:
        program = list(input.split(",").integers)
        if not self.testing:
            # before running the program, replace position 1 with the value 12 and replace position 2 with the value 2
            program[1] = 12
            program[2] = 2
        code = intcode.IntCode(program)
        code.run()
        return int(code.memory.read(0))

    def part_two(self, input: utils.Input) -> str | int:
        target = 19690720
        possibles = list(range(100))
        original = list(input.split(",").integers)
        for noun in possibles:
            for verb in possibles:
                program = original[:]
                program[1:3] = noun, verb
                code = intcode.IntCode(program)
                with suppress(intcode.BadOpcode, intcode.SegFault, intcode.NoInput):
                    code.run()
                    if code.memory.read(0) == target:
                        return 100 * noun + verb
        return -1


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=2,
        test_answers=("30", "no-answer"),
        test_input="""1,1,1,4,99,5,6,0,99""",
    )
    runner.cli()
