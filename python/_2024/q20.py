import itertools

import utils

type Point = utils.Point
type Steps = int


def how_many_shortcuts(best: dict[Point, Steps], max_steps: int, saving_goal: int) -> int:
    ans = 0
    for found, other in itertools.combinations(best, 2):
        dist = utils.manhattan_2d(found, other)
        if not (1 < dist <= max_steps):
            continue
        ans += abs(best[other] - best[found]) - dist >= saving_goal
    return ans


class Puzzle(utils.Puzzle):
    """
    Race from start to finish. What's the best score?

    How many unique cheats are there?
    """

    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        """
        Part 1: Skip through a single wall (2 steps).

        Part 2: Skip through up to 19 walls (20 steps).
        """
        grid = input.grid()
        start = grid.find("S")
        end = grid.find("E")
        best = utils.dijkstra_best_score(grid, start, end, unmovable="#")
        p1 = how_many_shortcuts(best, 2, saving_goal=2 if self.testing else 100)
        p2 = how_many_shortcuts(best, 20, saving_goal=50 if self.testing else 100)
        return p1, p2


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=20,
        both=True,
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
