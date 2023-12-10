import aocd
import matplotlib
import networkx as nx

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
    # TODO: using networkx to determine the path is incredibly slow, re-write as
    # dfs
    graph = grid.to_graph(
        diagonal=False, weighted=False, directed=True, is_connected_func=is_connected
    )
    from_, to_ = graph[start].keys()
    all_paths = list(nx.all_simple_paths(graph, from_, to_))
    longest = max(all_paths, key=len)

    farthest_point = (len(longest) + 1) // 2
    trapped_squares = 0
    loop = set(longest)
    # Draw a polygon using the loop points, and then check all points in the grid
    # to see if they are inside or outside the polgygon.
    poly = matplotlib.path.Path(longest)
    trapped_squares = sum(1 for point in grid if point not in loop and poly.contains_point(point))
    return farthest_point, trapped_squares


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
