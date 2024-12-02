from __future__ import annotations

import aocd
import networkx as nx

from utils import Grid, Point


def build_graph(data: str) -> tuple[nx.DiGraph, Point, Point, Point]:
    grid = Grid.from_number_string(data)
    original_x, original_y = max(grid)
    new_grid = grid.replicate(right=5, down=5)
    for x, y in new_grid:
        new_grid[x, y] += (x // (original_x + 1)) + (y // (original_y + 1))
        while new_grid[x, y] > 9:
            new_grid[x, y] -= 9
    return new_grid.to_graph(), (0, 0), (original_x, original_y), max(new_grid)


def part_one(graph: nx.DiGraph, start: Point, target: Point) -> int:
    return nx.shortest_path_length(graph, source=start, target=target, weight="weight")


def part_two(graph: nx.DiGraph, start: Point, target: Point) -> int:
    return nx.shortest_path_length(graph, source=start, target=target, weight="weight")


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
