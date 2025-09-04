from itertools import combinations
import z3
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        hailstones = []
        for line in input.lines().strings:
            pos, vel = line.split(" @ ")
            x, y, z = [int(p) for p in pos.split(", ")]
            vx, vy, vz = [int(v) for v in vel.split(", ")]
            hailstones.append(((x, y, z), (vx, vy, vz)))
        return sum(solve_xy(h1, h2, lower, upper) for h1, h2 in combinations(hailstones, 2))

    def part_two(self, input: utils.Input) -> str | int:
        hailstones = []
        for line in input.lines().strings[:3]:
            pos, vel = line.split(" @ ")
            x, y, z = [int(p) for p in pos.split(", ")]
            vx, vy, vz = [int(v) for v in vel.split(", ")]
            hailstones.append(((x, y, z), (vx, vy, vz)))
        return solve_xyz(*hailstones)


puzzle = Puzzle(
    year=2023,
    day=24,
    test_answers=("2", "47"),
    test_input="""\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""",
)

if __name__ == "__main__":
    puzzle.cli()
