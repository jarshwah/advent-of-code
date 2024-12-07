import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid()
        visited, _ = wander(grid)
        return len({v[0] for v in visited})

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.grid()
        visited, _ = wander(grid)
        points_crossed = {v[0] for v in visited}
        guard = grid.find("^")
        points_crossed.remove(guard)
        num_loops = 0
        for point in points_crossed:
            grid[point] = "#"
            _, in_loop = wander(grid)
            if in_loop:
                num_loops += 1
            grid[point] = "."
        return num_loops


def wander(grid: utils.Grid[str]) -> tuple[set[tuple[utils.Point, utils.Point]], bool]:
    guard = grid.find("^")
    direction = utils.UP
    visited = {(guard, direction)}
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
