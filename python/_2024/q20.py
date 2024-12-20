import itertools
from collections import Counter

import utils

type Point = utils.Point
type Steps = int


def how_many_shortcuts(best: dict[Point, Steps], max_steps: int, saving_goal: int) -> int:
    cheats: Counter[int] = Counter()
    for found, other in itertools.combinations(best, 2):
        dist = utils.manhattan_2d(found, other)
        if not (1 < dist <= max_steps):
            continue
        saving = abs(best[other] - best[found]) - dist
        if saving >= saving_goal:
            cheats[saving] += 1
    return sum(cheats.values())


class Puzzle(utils.Puzzle):
    """
    Race from start to finish. What's the best score?
    """

    def part_one(self, input: utils.Input) -> str | int:
        """
        How many shortcuts can you take with wallhacks for 2 steps?
        """
        saving_goal = 2 if self.testing else 100
        grid = input.grid()
        start = grid.find("S")
        end = grid.find("E")
        best = utils.dijkstra_best_score(grid, start, end, unmovable="#")
        return how_many_shortcuts(best, 2, saving_goal)

    def part_two(self, input: utils.Input) -> str | int:
        """
        How many shortcuts can you take with wallhacks for 20 steps?
        """
        saving_goal = 50 if self.testing else 100
        grid = input.grid()
        start = grid.find("S")
        end = grid.find("E")
        best = utils.dijkstra_best_score(grid, start, end, unmovable="#")
        return how_many_shortcuts(best, 20, saving_goal)


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=20,
        test_answers=("44", "285"),
        test_input="""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""",
    )
    runner.cli()


n = [
    32,
    31,
    29,
    39,
    25,
    23,
    20,
    19,
    12,
    14,
    12,
    22,
    4,
    3,
]
