from __future__ import annotations

import aocd
import networkx as nx
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra

from utils import Grid, Point


def build_graph(data: str) -> tuple[nx.DiGraph, Point, Point, Point]:
    grid = Grid(rows=((int(n) for n in row) for row in data.splitlines()))
    first_stop = max(grid)
    lx = first_stop[0] + 1
    ly = first_stop[1] + 1
    for y in range(ly):
        for x in range(lx):
            for yd in range(0, 5):
                for xr in range(0, 5):
                    if yd == xr == 0:
                        continue
                    newy = ly * yd + y
                    newx = lx * xr + x
                    weight = grid[x, y] + xr + yd
                    if weight > 9:
                        weight -= 9
                    grid[newx, newy] = weight

    graph = nx.DiGraph()
    for point in grid:
        neighbours = grid.get_neighbours(point)
        for nb in neighbours:
            graph.add_edge(point, nb, weight=grid[nb])
    return graph, (0, 0), first_stop, max(grid)


def part_one(graph: nx.DiGraph, start: Point, target: Point) -> int:
    return single_source_dijkstra(graph, start, target)[0]


def part_two(graph: nx.DiGraph, start: Point, target: Point) -> int:
    return single_source_dijkstra(graph, start, target)[0]


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
    graph, start, p1, p2 = build_graph(test_input)
    answer_1 = part_one(graph, start, p1)
    answer_2 = part_two(graph, start, p2)
    assert answer_1 == 40, answer_1
    assert answer_2 == 315, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=15, year=2021)
    graph, start, p1, p2 = build_graph(data)
    print("Part 1: ", part_one(graph, start, p1))
    print("Part 2: ", part_two(graph, start, p2))
