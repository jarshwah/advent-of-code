import utils


def score(grid: utils.Grid[str], box: str = "O") -> int:
    gps = 0
    for row, col in grid:
        if grid[row, col] == box:
            gps += 100 * row + col
    return gps


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid_map, instructions = input.group(sep="\n").strings
        moves = "".join(instructions)
        grid = utils.Grid(rows=grid_map)
        robot = grid.find("@")
        for move in moves:
            # grid.print()
            new_robot = utils.moves(robot, move)
            if grid[new_robot] == "#":
                continue
            if grid[new_robot] == ".":
                grid[robot] = "."
                grid[new_robot] = "@"
                robot = new_robot
                continue

            # it's a box! can we push it.. recursively?
            path = [new_robot]
            while True:
                new_box = utils.moves(path[-1], move)
                if grid[new_box] == "#":
                    path = []
                    break
                if grid[new_box] == ".":
                    path.append(new_box)
                    break
                path.append(new_box)

            if not path:
                # Couldn't push them, we hit a wall
                continue

            grid[robot] = "."
            grid[new_robot] = "@"
            grid[path[-1]] = "O"
            robot = new_robot
        return score(grid)

    def part_two(self, input: utils.Input) -> str | int:
        grid_map, instructions = input.group(sep="\n").strings
        # moves = "".join(instructions)
        expanded_map = []
        for row in grid_map:
            expanded_map.append(
                row.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
            )
        grid = utils.Grid(rows=expanded_map)
        grid.print()
        # TODO: ... finish this
        # robot = grid.find("@")
        return score(grid, "[")


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=15,
        test_answers=("2028", "9021"),
        test_input="""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""",
        test_input_2="""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""",
    )
    runner.cli()
