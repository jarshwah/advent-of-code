import aocd
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


def both_parts(raw: str) -> tuple[int, int]:
    grid = utils.Input(raw).grid()
    start = utils.only(p for p in grid if grid[p] == "S")

    # Determine the beginning and end of the path
    source = None
    target = None
    for nb in "|-LJ7F":
        d1, d2 = NEIGHBOURS[nb]
        source = utils.point_add(start, d1)
        target = utils.point_add(start, d2)
        if is_connected(grid, start, source) and is_connected(grid, start, target):
            break

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


def test():
    a1, a2 = both_parts(
        """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
    )

    assert a1 == 23, a1
    assert a2 == 4, a2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=10, year=2023)
    a1, a2 = both_parts(data)
    print("Part 1: ", a1)
    print("Part 2: ", a2)
