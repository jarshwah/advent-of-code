from collections import deque

import aocd
import networkx as nx

import utils

DIRS = {
    ">": [utils.RIGHT],
    "<": [utils.LEFT],
    "^": [utils.UP],
    "v": [utils.DOWN],
    "#": [],
    ".": utils.DIRECTIONS_4,
}


def part_one(raw: str) -> int:
    grid = utils.Input(raw).grid()
    path_found = 0
    start = (0, 1)
    target = (grid.height - 1, grid.width - 2)
    queue = deque([(start, 0, set())])
    while queue:
        curr, steps, path = queue.popleft()
        if curr in path:
            continue
        curr_tile = grid[curr]
        if curr == target:
            path_found = max(path_found, steps)
        directions = DIRS.get(curr_tile)
        for nb in grid.get_neighbours(curr, directions=directions):
            queue.appendleft((nb, steps + 1, path | {curr}))

    return path_found


def to_graph(grid: utils.Grid) -> dict[utils.Point, set[utils.Point]]:
    # Rather than creating a node per point, create a node per non-branching path.
    graph = nx.Graph()
    start = (0, 1)
    queue = deque([(start, start, 0)])
    seen = set()
    while queue:
        connected_to, curr, weight = queue.popleft()
        while True:
            seen.add(curr)
            nbs = [nb for nb in grid.get_neighbours(curr) if grid[nb] != "#" and nb not in seen]
            if len(nbs) == 1:
                curr = nbs[0]
                weight += 1
                continue
            graph.add_edge(connected_to, curr, weight=weight)
            for nb in nbs:
                # Start with a weight of 1, not 0
                queue.append((curr, nb, 1))
            break
    return graph


def part_two(raw: str) -> int:
    grid = utils.Input(raw).grid()
    path_found = 0
    graph = to_graph(grid)
    start = (0, 1)
    target = (grid.height - 1, grid.width - 2)
    queue = deque([(start, 0, frozenset(set()))])
    while queue:
        curr, steps, path = queue.popleft()
        if curr in path:
            continue
        if curr == target:
            path_found = max(path_found, steps)
        for nb, attrs in graph[curr].items():
            queue.appendleft((nb, steps + attrs["weight"], frozenset(path | {curr})))
    return path_found


def test():
    test_input = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 94, answer_1
    assert answer_2 == 154, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=23, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
