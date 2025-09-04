import intcode

import utils

type Point = utils.Point

BLACK = 0
WHITE = 1
TURNS = {
    0: utils.turn_left,
    1: utils.turn_right,
}
OUT = {BLACK: " ", WHITE: "#"}


class Puzzle(utils.Puzzle):
    """--- Day 11: Space Police ---"""

    def both_parts(self, input: utils.Input) -> tuple[int | str, int | str]:
        lengths = []
        # 0: starting black -> output num uniq visited squares
        # 1: starting white -> output 8 char message (OCR)
        for starting in [0, 1]:
            program = input.split(",").numbers
            brain = intcode.IntCode(program)
            robot: Point = (0, 0)
            hull: dict[Point, int] = {robot: starting}
            facing = utils.DIRECTIONS_ASCII["^"]
            while not brain._halted:
                colour = hull.get(robot, BLACK)
                brain.input.write(colour)
                paint = next(brain.output)
                turn = TURNS[next(brain.output)]
                hull[robot] = paint
                facing = turn(facing)
                robot = utils.move(robot, facing)
            lengths.append(len(hull))

        maxr = max(p[0] for p in hull)
        maxc = max(p[1] for p in hull)
        message = ["\n"]
        for rn in range(maxr + 1):
            for rc in range(maxc + 1):
                ch = OUT[hull.get((rn, rc), BLACK)]
                message.append(ch)
            message.append("\n")

        return lengths[0], "".join(message)


puzzle = Puzzle(
    year=2019,
    day=11,
    both=True,
    no_tests=True,
    test_answers=("", ""),
    test_input="""""",
)

if __name__ == "__main__":
    puzzle.cli()
