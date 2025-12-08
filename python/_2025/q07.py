import sys
from collections import deque
from functools import cache

import utils

sys.setrecursionlimit(10000)


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid()
        start = grid.find("S")
        splitters = set(grid.find_all("^"))
        visited: set[utils.Point] = set()
        beams = deque([start])
        while beams:
            beam = beams.popleft()
            if beam in visited:
                continue
            visited.add(beam)

            if beam in splitters:
                beams.extend(
                    [utils.sum_points(beam, utils.LEFT), utils.sum_points(beam, utils.RIGHT)]
                )
                continue

            for nb in grid.neighbours(beam, directions=[utils.DOWN]):
                grid[beam] = "|"
                grid.save_frame()
                beams.append(nb)
        if self.animate:
            grid.draw_frames(
                {
                    "^": utils.ColorRGB.Yellow.value,
                    ".": utils.BackgroundColor.value,
                    "|": utils.ColorRGB.PurpleLight.value,
                }
            )
            grid.render_video("2025-Q07-Part1", framerate=500)
        return len(visited & splitters)

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.grid()
        start = grid.find("S")
        splitters = set(grid.find_all("^"))

        @cache
        def recurse(beam: utils.Point) -> int:
            down = utils.sum_points(beam, utils.DOWN)
            if down not in grid:
                return 1
            if beam in splitters:
                left = utils.sum_points(beam, utils.LEFT)
                right = utils.sum_points(beam, utils.RIGHT)
                return recurse(left) + recurse(right)
            return recurse(down)

        return recurse(start)


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=7,
        test_answers=("21", "40"),
        test_input=""".......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""",
    )
    runner.cli()
