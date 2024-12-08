import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Walk the guard around the board, turning right at each obstruction, and count
        the visited points before walking off the grid.
        """
        grid = input.grid()
        guard = grid.find("^")
        direction = utils.UP
        visited, _ = wander(grid, guard, direction)
        return len({v[0] for v in visited})

    def part_two_alt(self, input: utils.Input) -> str | int:
        """
        Walk the guard around the board, turning right at each obstruction.

        As we meet an available space, place an obstruction there, and simulate the new
        path. If the new path loops, count it.
        """
        grid = input.grid()
        guard = grid.find("^")
        direction = utils.UP
        visited = {(guard, direction)}
        # We need to maintain a history of the blocked paths, so we don't attempt to
        # simulate it again coming from a different direction (as we wouldn't) have
        # arrived there.
        history = set()
        loops = set()
        while guard in grid:
            new_guard = utils.point_add(guard, direction)
            if new_guard not in grid:
                break
            if grid[new_guard] == ".":
                # If this is a free space and we haven't already tried blocking it, simulate
                # a new path.
                if new_guard not in history:
                    grid[new_guard] = "#"
                    _, in_loop = wander(grid, guard, direction, visited)
                    grid[new_guard] = "."
                    if in_loop:
                        loops.add(new_guard)
                guard = new_guard
            visited.add((guard, direction))
            history.add(guard)
            if grid[new_guard] == "#":
                direction = utils.turn_right(direction)
                continue
        return len(loops)

    def part_two(self, input: utils.Input) -> str | int:
        """
        For each visited spot in the original path, place an obstruction, and detect if
        the guard gets into a loop.
        """
        grid = input.grid()
        guard = grid.find("^")
        direction = utils.UP
        visited, _ = wander(grid, guard, direction)
        points_crossed = {v[0] for v in visited}
        points_crossed.remove(guard)
        num_loops = 0
        for point in points_crossed:
            grid[point] = "#"
            _, in_loop = wander(grid, guard, direction)
            if in_loop:
                num_loops += 1
            grid[point] = "."
        return num_loops


def wander(
    grid: utils.Grid[str],
    guard: utils.Point,
    direction: utils.Point,
    prev_visited: set[tuple[utils.Point, utils.Point]] = set(),
) -> tuple[set[tuple[utils.Point, utils.Point]], bool]:
    visited = set(prev_visited) | {(guard, direction)}
    while guard in grid:
        new_pos = utils.point_add(guard, direction)
        if new_pos not in grid:
            break
        if grid[new_pos] == "#":
            direction = utils.turn_right(direction)
            continue
        guard = new_pos
        if (guard, direction) in visited:
            return visited, True
        visited.add((guard, direction))
    return visited, False


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=6,
        test_answers=("41", "6"),
        test_input="""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""",
    )
    runner.cli()
