import itertools
import typing as t

import aocd
import networkx as nx
from parse import compile

outer_parser = compile("{} bag")
inner_parser = compile("{:d} {} bag")


def build_graph(rules: t.List[str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for rule in rules:
        outer_colour = outer_parser.search(rule)[0]
        inside = [color for color in inner_parser.findall(rule)]
        bags = [color[1] for color in inside]
        weights = [color[0] for color in inside]
        graph.add_weighted_edges_from(zip(itertools.repeat(outer_colour), bags, weights))
    return graph


def part_one(graph: nx.DiGraph) -> int:
    return len(nx.ancestors(graph, "shiny gold"))


def part_two(graph: nx.DiGraph) -> int:
    def counter(node: str) -> int:
        total = 0
        for next_node, attrs in graph[node].items():
            total += attrs["weight"] + (counter(next_node) * attrs["weight"])
        return total

    return counter("shiny gold")


if __name__ == "__main__":
    data = aocd.get_data(day=7, year=2020).splitlines()
    g = build_graph(data)
    print("Part 1: ", part_one(g))
    print("Part 2: ", part_two(g))
