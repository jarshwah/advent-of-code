import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid()
        grid = tilt_north(grid)
        return north_load(grid)

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.grid()

        cycles = {}
        n = 0
        target = 1e9
        while n < target:
            grid = tilt_north(grid).rotate(1)
            grid = tilt_north(grid).rotate(1)
            grid = tilt_north(grid).rotate(1)
            grid = tilt_north(grid).rotate(1)
            key = grid.hash_key()
            if key in cycles:
                first_seen = cycles[key]
                where = n - first_seen
                inc = (target - n) // where
                n += inc * where
            else:
                cycles[key] = n
            n += 1
        return north_load(grid)


puzzle = Puzzle(
    year=2023,
    day=14,
    test_answers=("136", "64"),
    test_input="""\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""",
)

if __name__ == "__main__":
    puzzle.cli()
