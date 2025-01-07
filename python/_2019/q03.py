from collections.abc import Sequence

import utils

type Point = utils.Point


def wire_points(wires: Sequence[str], curr: Point) -> dict[Point, int]:
    points = {}
    step = 0
    for vec in wires:
        d = utils.DIRECTIONS_LETTERS[vec[0]]
        for _ in range(int(vec[1:])):
            step += 1
            curr = utils.point_add(curr, d)
            if curr in points:
                continue
            points[curr] = step
    return points


class Puzzle(utils.Puzzle):
    """--- Day 3: Crossed Wires ---"""

    def part_one(self, input: utils.Input) -> str | int:
        w1, w2 = input.group("\n", ",").strings
        start = (0, 0)
        cross_overs = set(wire_points(w1, start).keys()) & set(wire_points(w2, start).keys())
        return min(utils.manhattan(start, xo) for xo in cross_overs)

    def part_two(self, input: utils.Input) -> str | int:
        w1, w2 = input.group("\n", ",").strings
        start = (0, 0)
        p1 = wire_points(w1, start)
        p2 = wire_points(w2, start)
        return min(steps1 + p2.get(pp, int(1e9)) for pp, steps1 in p1.items())


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=3,
        test_answers=("159", "610"),
        test_input="""R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83""",
    )
    runner.cli()
