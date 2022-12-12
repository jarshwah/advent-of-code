import aocd
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
    graph = nx.DiGraph()
    for point in grid:
        for neighbour in grid.get_neighbours(point):
            if grid[point] >= grid[neighbour] - 1:
                graph.add_edge(point, neighbour)
    return min(
        nx.shortest_path_length(graph, source=start, target=end)
        for start in possible_starts
        if nx.has_path(graph, start, end)
    )


def part_one(raw: str) -> int:
    return solve(raw, all_lowest=False)


def part_two(raw: str) -> int:
    return solve(raw, all_lowest=True)


def test():
    test_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 31, answer_1
    assert answer_2 == 29, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=12, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
