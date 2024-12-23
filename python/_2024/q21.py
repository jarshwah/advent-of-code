from collections.abc import Sequence
from functools import cache

from networkx.algorithms.shortest_paths import (  # type: ignore [attr-defined]
    all_pairs_all_shortest_paths,
)

import utils

type Point = utils.Point
type DirStr = str
type Button = str
type AdjacencyMatrix = dict[Button, dict[Button, Sequence[DirStr]]]


def get_keygrid() -> utils.Grid[str]:
    grid = utils.Grid.from_string("""789
456
123
#0A""")
    del grid.points[grid.find("#")]
    return grid


def get_dirgrid() -> utils.Grid[str]:
    grid = utils.Grid.from_string("""#^A
<v>""")

    del grid.points[grid.find("#")]
    return grid


def path_to_dirstring(path: list[Point]) -> DirStr:
    """
    Convert a path of points to a string of directions.
    """
    moves = [utils.moved(start, end) for start, end in zip(path, path[1:])]
    return "".join(moves)


def trim_paths(paths: Sequence[DirStr]) -> Sequence[DirStr]:
    """
    Remove any path with more than two turns.

    >^> is inefficient because it requires more button presses than >>^ from a remote terminal.
    """
    trimmed = []
    for path in paths:
        turns = 0
        for d1, d2 in zip(path, path[1:]):
            if d1 != d2:
                turns += 1
        if turns < 2:
            trimmed.append(path)
    return trimmed


def get_paths(grid: utils.Grid[str]) -> AdjacencyMatrix:
    """
    Get all optimised shortest paths between all points on the grid.
    """
    graph = grid.to_graph(directed=False, weighted=False)
    adjacency: AdjacencyMatrix = {}
    paths = all_pairs_all_shortest_paths(graph)
    for source, targets in paths:
        adjacency[grid[source]] = {}
        for target, paths in targets.items():
            adjacency[grid[source]][grid[target]] = trim_paths(
                [path_to_dirstring(path) for path in paths]
            )
    return adjacency


class Puzzle(utils.Puzzle):
    keygrid = get_keygrid()
    dirgrid = get_dirgrid()
    keygraph = get_paths(keygrid)
    dirgraph = get_paths(dirgrid)

    def part_one(self, input: utils.Input) -> str | int:
        KPATH = self.keygraph
        DPATH = self.dirgraph
        codes = input.lines().strings

        @cache
        def press_number(start_from: str, go_to: str, panel_num: int, keypad: bool) -> int:
            if panel_num == 0:
                # We can press any button in 1 move as a human
                return 1

            if start_from == go_to:
                # We can press A again to hit the same button.
                return 1

            paths = KPATH[start_from][go_to] if keypad else DPATH[start_from][go_to]
            presses: list[int] = []
            for path in paths:
                cost = 0
                for sf, gt in zip("A" + path, path + "A"):
                    cost += press_number(sf, gt, panel_num - 1, False)
                presses.append(cost)
            return min(presses)

        ans = 0
        for code in codes:
            num = 0
            for start_from, go_to in zip("A" + code, code):
                num += press_number(start_from, go_to, 3, True)
            ans += num * int(code[:3])
        return ans

    def part_two(self, input: utils.Input) -> str | int:
        KPATH = self.keygraph
        DPATH = self.dirgraph
        codes = input.lines().strings

        @cache
        def press_number(start_from: str, go_to: str, panel_num: int, keypad: bool) -> int:
            if panel_num == 0:
                # We can press any button in 1 move as a human
                return 1

            if start_from == go_to:
                # We can press A again to hit the same button.
                return 1

            paths = KPATH[start_from][go_to] if keypad else DPATH[start_from][go_to]
            presses: list[int] = []
            for path in paths:
                cost = 0
                for sf, gt in zip("A" + path, path + "A"):
                    cost += press_number(sf, gt, panel_num - 1, False)
                presses.append(cost)
            return min(presses)

        ans = 0
        for code in codes:
            num = 0
            for start_from, go_to in zip("A" + code, code):
                num += press_number(start_from, go_to, 26, True)
            ans += num * int(code[:3])
        return ans


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=21,
        test_answers=("126384", "154115708116294"),
        test_input="""029A
980A
179A
456A
379A""",
    )
    runner.cli()
