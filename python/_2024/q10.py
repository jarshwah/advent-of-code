import sys

import utils

sys.setrecursionlimit(10000)


def trail_score(
    grid: utils.Grid[int],
    curr_position: utils.Point,
    scores: dict[utils.Point, set[utils.Point]],
) -> set[utils.Point]:
    """
    Returns a set of all the 9's reachable from the current position.
    """
    if grid[curr_position] == 9:
        return {curr_position}

    if curr_position in scores:
        return scores[curr_position]

    nbs = [nb for nb in grid.get_neighbours(curr_position) if grid[nb] == grid[curr_position] + 1]
    scores[curr_position] = set.union(set(), *(trail_score(grid, nb, scores) for nb in nbs))
    return scores[curr_position]


def trail_rating(
    grid: utils.Grid[int],
    curr_position: utils.Point,
    scores: dict[utils.Point, int],
) -> int:
    """
    Returns the number of paths to 9's reachable from the current position.
    """
    if grid[curr_position] == 9:
        return 1

    if curr_position in scores:
        return scores[curr_position]

    nbs = [nb for nb in grid.get_neighbours(curr_position) if grid[nb] == grid[curr_position] + 1]
    scores[curr_position] = sum(trail_rating(grid, nb, scores) for nb in nbs)
    return scores[curr_position]


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Score: number of 9's reachable from a 0.
        """
        grid = input.grid_int()
        trailheads = [point for point in grid if grid[point] == 0]
        scores: dict[utils.Point, set[utils.Point]] = {}
        return sum(len(trail_score(grid, th, scores)) for th in trailheads)

    def part_two(self, input: utils.Input) -> str | int:
        """
        Score: number of paths to 9's reachable from a 0.
        """
        grid = input.grid_int()
        trailheads = [point for point in grid if grid[point] == 0]
        scores: dict[utils.Point, int] = {}
        return sum(trail_rating(grid, th, scores) for th in trailheads)


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=10,
        test_answers=("36", "81"),
        test_input="""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""",
    )
    runner.cli()
