from __future__ import annotations

import aocd
import networkx as nx
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra

from utils import Grid, Point


def build_graph(data: str) -> tuple[nx.DiGraph, Point, Point, Point]:
    grid = Grid(rows=((int(n) for n in row) for row in data.splitlines()))
    first_stop = max(grid)
    for y in range(first_stop[1]):  # 9
        for x in range(first_stop[0]):  # 9
            for n in range(1, 5):  # 4
                # increase size of grid down
                newy = first_stop[1] * n + y + 1  # 9 * 4 (36) + 9 (45) + 1 = 46
                # increase size of grid right
                newx = first_stop[0] * n + x + 1  # 9 * 4 (36) + 9 (45) + 1 = 46
                nweight = grid[x, y] + n
                if nweight > 9:
                    nweight -= 9
                grid[x, newy] = nweight
                grid[newx, y] = nweight
                grid[newx, newy] = nweight

    graph = nx.DiGraph()
    edge_count = 0
    for point in grid:
        neighbours = grid.get_neighbours(point)
        for nb in neighbours:
            edge_count += 1
            graph.add_edge(point, nb, weight=grid[nb])
    print(edge_count)
    return graph, (0, 0), first_stop, max(grid)


def part_one(data: str) -> int:
    graph, start, end, _ = build_graph(data)
    shortest = single_source_dijkstra(graph, start, end)
    return shortest[0]


def part_two(data: str) -> int:
    graph, start, _, end = build_graph(data)
    shortest = single_source_dijkstra(graph, start, end)
    return shortest[0]


def test():
    test_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 40, answer_1
    assert answer_2 == 315, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=15, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
