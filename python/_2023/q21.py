from collections import deque
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        for rn, row in enumerate(input.string.splitlines()):
            for cn, char in enumerate(row):
                if char == "S":
                    start = (rn, cn)
                    break
        return solve(raw, steps, start)

    def part_two(self, input: utils.Input) -> str | int:
        # expand the grid so it's big enough to do the 3 runs
        rows = []
        size = 0
        for _ in range(5):
            for row in input.string.splitlines():
                size = len(row)
                rows.append(row * 5)
        big_raw = "\n".join(rows)

        # Assume we begin right in the center of the grid. Solve confirms a match.
        STEPS_A = size // 2
        STEPS_B = size + STEPS_A
        STEPS_C = size + STEPS_B
        # print(f"{STEPS_A=} {STEPS_B=} {STEPS_C=}")
        # Start is in the center of the 3x3 grid
        big_start = (STEPS_C, STEPS_C)
        # print(f"{big_start=}")
        # Solve the first grid, then the second grid (larger, different parity), then the third (same parity as first)
        s1 = solve(big_raw, STEPS_A, big_start)
        s2 = solve(big_raw, STEPS_B, big_start)
        s3 = solve(big_raw, STEPS_C, big_start)
        # print(f"{s1=} {s2=} {s3=}")

        # Then we can compute the quadratic sequence (like we did for day 9, but math'd)
        # https://www.radfordmathematics.com/algebra/sequences-series/difference-method-sequences/quadratic-sequences.html
        N = (steps - STEPS_A) // size
        D1 = s2 - s1
        D2 = s3 - s2
        D3 = D2 - D1
        return s1 + N * D1 + N * (N - 1) // 2 * D3


puzzle = Puzzle(
    year=2023,
    day=21,
    test_answers=("", ""),
    test_input="""\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""",
)

if __name__ == "__main__":
    puzzle.cli()
