import itertools
from collections import Counter

import utils


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
        cheats: Counter[int] = Counter()
        best = utils.dijkstra_best_score(grid, start, end, unmovable="#")
        for found, other in itertools.combinations(best, 2):
            if utils.manhattan_2d(found, other) != 2:
                continue
            saving = abs(best[other] - best[found]) - 1
            if saving >= saving_goal:
                cheats[saving] += 1
        return sum(cheats.values())

    def part_two(self, input: utils.Input) -> str | int:
        """
        How many shortcuts can you take with wallhacks for 20 steps?
        """
        saving_goal = 50 if self.testing else 100
        grid = input.grid()
        start = grid.find("S")
        end = grid.find("E")
        cheats: Counter[int] = Counter()
        best = utils.dijkstra_best_score(grid, start, end, unmovable="#")
        for found, other in itertools.combinations(best, 2):
            dist = utils.manhattan_2d(found, other)
            if not (1 < dist <= 20):
                continue
            saving = abs(best[other] - best[found]) - dist
            if saving >= saving_goal:
                cheats[saving] += 1
        return sum(cheats.values())


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
