import sys

import utils

sys.setrecursionlimit(100000)


def trail_score(
    grid: utils.Grid[int],
    curr_position: utils.Point,
    scores: dict[utils.Point, set[utils.Point]],
) -> set[utils.Point]:
    if grid[curr_position] == 9:
        scores[curr_position] = {curr_position}

    if curr_position in scores:
        return scores[curr_position]

    nbs = [nb for nb in grid.get_neighbours(curr_position) if grid[nb] == grid[curr_position] + 1]
    scores[curr_position] = set()
    for nb in nbs:
        scores[curr_position] |= trail_score(grid, nb, scores)
    return scores[curr_position]


def trail_rating(
    grid: utils.Grid[int],
    curr_position: utils.Point,
    scores: dict[utils.Point, int],
) -> int:
    if grid[curr_position] == 9:
        return 1

    if curr_position in scores:
        return scores[curr_position]

    nbs = [nb for nb in grid.get_neighbours(curr_position) if grid[nb] == grid[curr_position] + 1]
    scores[curr_position] = 0
    for nb in nbs:
        scores[curr_position] += trail_rating(grid, nb, scores)
    return scores[curr_position]


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Score: number of 9's reachable from a 0.

        34089 -> too high
        """
        grid = input.grid_int()
        trailheads = [point for point in grid if grid[point] == 0]
        tally = []
        scores: dict[utils.Point, set[utils.Point]] = {}
        for trailhead in trailheads:
            found = trail_score(grid, trailhead, scores)
            tally.append(len(found))
        return sum(tally)

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.grid_int()
        trailheads = [point for point in grid if grid[point] == 0]
        tally = []
        scores: dict[utils.Point, int] = {}
        for trailhead in trailheads:
            found = trail_rating(grid, trailhead, scores)
            tally.append(found)
        return sum(tally)


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
