import matplotlib

import utils

NEIGHBOURS = {
    "|": (utils.UP, utils.DOWN),
    "-": (utils.LEFT, utils.RIGHT),
    "L": (utils.UP, utils.RIGHT),
    "J": (utils.UP, utils.LEFT),
    "7": (utils.DOWN, utils.LEFT),
    "F": (utils.DOWN, utils.RIGHT),
    ".": (),
    "S": utils.DIRECTIONS_4,
}


def print_cycle(cycle: list[utils.Point], grid: utils.Grid):
    for point in cycle:
        print(grid[point], end="->")
    print()


def is_connected(grid: utils.Grid, check: utils.Point, target: utils.Point) -> bool:
    check_pipe = grid[check]
    target_pipe = grid[target]

    if "." in (check_pipe, target_pipe):
        return False

    direction = utils.point_subtract(target, check)
    match direction:
        case utils.UP if utils.DOWN in NEIGHBOURS[target_pipe]:
            return True
        case utils.DOWN if utils.UP in NEIGHBOURS[target_pipe]:
            return True
        case utils.LEFT if utils.RIGHT in NEIGHBOURS[target_pipe]:
            return True
        case utils.RIGHT if utils.LEFT in NEIGHBOURS[target_pipe]:
            return True

    return False


class Puzzle(utils.Puzzle):
    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        grid = input.grid()
        start = utils.only(p for p in grid if grid[p] == "S")

        # Determine the beginning and end of the path
        source = None
        target = None
        connected = []
        for nb in grid.get_neighbours(start):
            if is_connected(grid, start, nb):
                connected.append(nb)
        source, target = connected

        if not is_connected(grid, start, source) or not is_connected(grid, start, target):
            # Maybe we have the source and target reversed
            source, target = target, source

        assert source is not None and target is not None

        # There is only a single valid path, so no need to use A* to estimate,
        # or a queue to navigate
        path = [start, source]
        while True:
            check = path[-1]
            if check == target:
                farthest_point = len(path) // 2
                loop = set(path)
                poly = matplotlib.path.Path(path)
                trapped_squares = sum(
                    1 for point in grid if point not in loop and poly.contains_point(point)
                )
                return farthest_point, trapped_squares

            for nb in grid.get_neighbours(check, directions=NEIGHBOURS[grid[check]]):
                if nb == path[-2]:
                    continue
                path.append(nb)
                break


puzzle = Puzzle(
    year=2023,
    day=10,
    test_answers=("23", "4"),
    test_input="""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""",
    both=True,
)

if __name__ == "__main__":
    puzzle.cli()
