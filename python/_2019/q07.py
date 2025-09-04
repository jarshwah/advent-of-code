import itertools

import intcode

import utils


class Puzzle(utils.Puzzle):
    """--- Day 7: Amplification Circuit ---"""

    def part_one(self, input: utils.Input) -> str | int:
        program = input.split(",").numbers
        phase_settings = [0, 1, 2, 3, 4]
        best = 1
        for wombo in itertools.permutations(phase_settings, 5):
            output = 0
            for ith in range(5):
                runner = intcode.IntCode(program[::])
                runner.input.write(wombo[ith])
                runner.input.write(output)
                output = runner.run()[-1]
            best = max(best, output)
        return best

    def part_two(self, input: utils.Input) -> str | int:
        program = input.split(",").numbers
        phase_settings = [5, 6, 7, 8, 9]
        best = 1
        for wombo in itertools.permutations(phase_settings, 5):
            output = 0
            # Chain the inputs to the outputs, with callbacks on READ/WRITE to advance the
            # interpreter when performing IO.
            runners = [intcode.IntCode(program[::], name=f"Runner{i}") for i in range(5)]
            intcode.chain_intcode_io(*runners, loop=True)
            for runner, phase in zip(runners, wombo):
                runner.input.write(phase)

            first_runner = runners[0]
            first_runner.input.write(0)
            first_runner.run()
            output = runners[-1].output.dump()[-1]
            best = max(best, output)
        return best


puzzle = Puzzle(
    year=2019,
    day=7,
    test_answers=("43210", "139629729"),
    test_input="""3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0""",
    test_input_2="""3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5""",
)

if __name__ == "__main__":
    puzzle.cli()
