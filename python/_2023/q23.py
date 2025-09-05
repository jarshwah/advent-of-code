from collections import deque

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


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid()
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

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.grid()
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


puzzle = Puzzle(
    year=2023,
    day=23,
    test_answers=("94", "154"),
    test_input="""\
#.#####################
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
#####################.#""",
)

if __name__ == "__main__":
    puzzle.cli()
