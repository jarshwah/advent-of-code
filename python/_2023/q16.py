from collections import deque
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid()
        return num_energized(grid, (0, 0), utils.RIGHT)

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.grid()
        starting_positions = []
        for p in grid:
            if p[0] == 0:
                starting_positions.append((p, utils.DOWN))
            if p[1] == 0:
                starting_positions.append((p, utils.RIGHT))
            if p[0] == grid.height - 1:
                starting_positions.append((p, utils.UP))
            if p[1] == grid.width - 1:
                starting_positions.append((p, utils.LEFT))
        return max(num_energized(grid, start, direction) for start, direction in starting_positions)


puzzle = Puzzle(
    year=2023,
    day=16,
    test_answers=("46", "51"),
    test_input="""\
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""",
)

if __name__ == "__main__":
    puzzle.cli()
