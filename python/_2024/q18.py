import heapq
from copy import deepcopy
from typing import cast

import utils

type Point = utils.Point


class Puzzle(utils.Puzzle):
    """
    Simulate squares getting blocked over time.

    Test grid is 7x7.
    Real grid is 71x71.

    Make your way from the top-left to the bottom-right.
    """

    def part_one(self, input: utils.Input) -> str | int:
        """
        Simulate the first N corruptions and find the shortest path to the bottom-right.

        N = 12 for test, 1024 for real.

        The answer is the number of steps to reach the bottom-right.
        """
        is_test = input.data == self.test_input
        corruptions = cast(list[Point], input.split("\n").scan_ints())
        size = 7 if is_test else 71
        first = 12 if is_test else 1024
        grid = utils.Grid(rows=[["." for _ in range(size)] for _ in range(size)])
        for c, r in corruptions[:first]:
            grid[r, c] = "#"

        start = (0, 0)
        target = (size - 1, size - 1)
        dist = utils.manhattan(start, target)
        heap: list[tuple[int, int, Point]] = []
        seen: dict[Point, int] = {}
        heapq.heappush(heap, (dist, 0, start))
        while heap:
            _, t, position = heapq.heappop(heap)
            if position == target:
                seen[target] = min(seen.get(target, int(1e9)), t)
                continue
            if grid[position] == "#":
                continue
            if position in seen and seen[position] <= t:
                continue
            seen[position] = t
            for new_position in grid.get_neighbours(position):
                heapq.heappush(heap, (utils.manhattan(new_position, target), t + 1, new_position))
        return seen[target]

    def part_two(self, input: utils.Input) -> str | int:
        """
        Find the first corruption that makes the bottom-right unreachable.
        """
        is_test = input.data == self.test_input
        corruptions = cast(list[Point], input.split("\n").scan_ints())
        size = 7 if is_test else 71
        search_from = 12 if is_test else 1024
        empty_grid = utils.Grid(rows=[["." for _ in range(size)] for _ in range(size)])

        def build_grid(t: int) -> utils.Grid[str]:
            new_grid = deepcopy(empty_grid)
            for c, r in corruptions[:t]:
                new_grid[r, c] = "#"
            return new_grid

        def reachable(t: int) -> bool:
            grid = build_grid(t)
            start = (0, 0)
            target = (size - 1, size - 1)
            dist = utils.manhattan(start, target)
            heap: list[tuple[int, int, Point]] = []
            seen: dict[Point, int] = {}
            heapq.heappush(heap, (dist, 0, start))
            while heap:
                _, t, position = heapq.heappop(heap)
                if position == target:
                    return True
                if grid[position] == "#":
                    continue
                if position in seen and seen[position] <= t:
                    continue
                seen[position] = t
                for new_position in grid.get_neighbours(position):
                    heapq.heappush(
                        heap, (utils.manhattan(new_position, target), t + 1, new_position)
                    )
            return False

        # Binary search for the first unreachable
        min_search = search_from
        max_search = len(corruptions)
        while True:
            if min_search == max_search:
                break
            search = (min_search + max_search) // 2
            if reachable(search):
                min_search = search + 1
            else:
                max_search = search
        return ",".join(str(p) for p in corruptions[min_search - 1])


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=18,
        test_answers=("22", "6,1"),
        test_input="""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""",
    )
    runner.cli()
