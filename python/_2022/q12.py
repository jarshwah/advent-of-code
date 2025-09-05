import networkx as nx
import utils


def solve(raw: str, all_lowest: bool = False):
    rows = []
    possible_starts = set()
    end: utils.Point = (-1, -1)
    for rn, row in enumerate(raw.splitlines()):
        num_row = []
        for cn, col in enumerate(row):
            if col == "S":
                col = "a"
                possible_starts.add((rn, cn))
            if col == "E":
                end = (rn, cn)
                col = "z"
            if all_lowest and col == "a":
                possible_starts.add((rn, cn))
            num_row.append(ord(col))
        rows.append(num_row)
    grid = utils.Grid(rows=rows)

    def is_connected(grid: utils.Grid, a: utils.Point, b: utils.Point) -> bool:
        return grid[a] >= grid[b] - 1

    graph = grid.to_graph(weighted=False, is_connected_func=is_connected)
    return min(
        nx.shortest_path_length(graph, source=start, target=end)
        for start in possible_starts
        if nx.has_path(graph, start, end)
    )


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        return solve(raw, all_lowest=False)

    def part_two(self, input: utils.Input) -> str | int:
        return solve(raw, all_lowest=True)


puzzle = Puzzle(
    year=2022,
    day=12,
    test_answers=("31", "29"),
    test_input="""\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""",
)

if __name__ == "__main__":
    puzzle.cli()
