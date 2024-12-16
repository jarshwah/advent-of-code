import heapq
from copy import deepcopy

import utils

type Point = utils.Point


class Puzzle(utils.Puzzle):
    """
    Walk the grid from start to end.

    Each step costs 1. Each turn costs 1000.

    Find the cost of the shortest path, and the number of tiles that make up any shortest path.
    """

    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        grid = input.grid()
        start = grid.find("S")
        end = grid.find("E")
        direction = utils.RIGHT
        heap: list[tuple[int, Point, Point, set[Point], bool]] = []
        seen: dict[tuple[Point, Point], tuple[int, set[Point]]] = {}
        heapq.heappush(heap, (0, start, direction, set(), False))
        best_score = int(1e9)
        best_path: set[Point] = set()
        while heap:
            distance, position, direction, path, did_turn = heapq.heappop(heap)
            if position not in grid or grid[position] == "#":
                continue

            key = (position, direction)
            new_path = path | {position}

            if position == end and distance <= best_score:
                best_score = distance
                best_path = new_path if distance < best_score else best_path | new_path
                continue

            if key in seen:
                seen_distance, seen_path = seen[key]
                if seen_distance == distance and path != seen_path:
                    # If matching, combine the good paths
                    new_path |= seen_path
                    seen[key] = distance, new_path
                elif seen_distance > distance:
                    # If better, replace the path
                    seen[key] = distance, new_path
                else:
                    continue
                # We must continue to explore from here now that we have our bigger path

            seen[key] = distance, new_path
            heapq.heappush(
                heap,
                (distance + 1, utils.point_add(position, direction), direction, new_path, False),
            )
            if not did_turn:
                # Stop trying to turn back
                heapq.heappush(
                    heap, (distance + 1000, position, utils.turn_right(direction), new_path, True)
                )
                heapq.heappush(
                    heap, (distance + 1000, position, utils.turn_left(direction), new_path, True)
                )

        return best_score, len(best_path)


def print_path(grid, path, loc, dir):  # type: ignore
    # Debug the path
    new_grid = deepcopy(grid)
    for point in path:
        new_grid[point] = "v"
    new_grid[loc] = {
        utils.UP: "^",
        utils.DOWN: "v",
        utils.LEFT: "<",
        utils.RIGHT: ">",
    }[dir]
    new_grid.print()


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=16,
        both=True,
        test_answers=("7036", "45"),
        test_input="""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""",
    )
    runner.cli()
