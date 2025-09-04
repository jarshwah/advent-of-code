import heapq
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid_int()

        return get_heat(
            grid=grid,
            start=(0, 0),
            goal=(grid.height - 1, grid.width - 1),
            start_direction=utils.RIGHT,
            max_forward=3,
            min_forward=1,
        )

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.grid_int()
        return get_heat(
            grid=grid,
            start=(0, 0),
            goal=(grid.height - 1, grid.width - 1),
            start_direction=utils.RIGHT,
            max_forward=10,
            min_forward=4,
        )


puzzle = Puzzle(
    year=2023,
    day=17,
    test_answers=("102", "94"),
    test_input="""\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""",
)

if __name__ == "__main__":
    puzzle.cli()
