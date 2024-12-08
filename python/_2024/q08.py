import itertools
from collections import defaultdict

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Find the number of anti-nodes formed by pairs of antennas.

        An anti-node projects backwards from an antenna the same distance and direction
        as the distance between another antenna of the same name.
        """
        grid = input.grid()
        antennas: dict[str, set[utils.Point]] = defaultdict(set)
        for point in grid:
            if grid[point] != ".":
                antennas[grid[point]].add(point)
        antinodes = set()
        for antenna_name in antennas:
            for a1, a2 in itertools.permutations(antennas[antenna_name], r=2):
                if (anti := utils.point_add(a1, utils.point_subtract(a1, a2))) in grid:
                    antinodes.add(anti)
        return len(antinodes)

    def part_two(self, input: utils.Input) -> str | int:
        """
        Find the number of anti-nodes formed by pairs of antennas.

        An anti-node projects backwards from an antenna the same distance and direction
        as the distance between another antenna of the same name. But it also keeps projecting
        backwards until it runs off the grid.

        Any antennas that have at least one pair are also themselves anti-nodes.
        """
        grid = input.grid()
        antennas: dict[str, set[utils.Point]] = defaultdict(set)
        for point in grid:
            if grid[point] != ".":
                antennas[grid[point]].add(point)
        antinodes = set()
        for antenna_name in antennas:
            for a1, a2 in itertools.permutations(antennas[antenna_name], r=2):
                # IF the antenna isn't singular, it also forms an anti-node.
                antinodes.add(a1)
                diff = utils.point_subtract(a1, a2)
                while (a1 := utils.point_add(a1, diff)) in grid:
                    antinodes.add(a1)
        return len(antinodes)


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=8,
        test_answers=("14", "9"),
        test_input="""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""",
        test_input_2="""T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........""",
    )
    runner.cli()
