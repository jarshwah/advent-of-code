import math
import random
from collections import Counter

import aocd
import networkx as nx

import utils


def part_one(raw: str) -> int:
    graph = nx.Graph()
    for line in utils.Input(raw).lines().strings:
        from_node, rest = line.split(":")
        to_nodes = rest.split()
        for node in to_nodes:
            graph.add_edge(from_node, node)
    graph.remove_edges_from(nx.minimum_edge_cut(graph))
    return math.prod(map(len, nx.connected_components(graph)))


def part_one_alt(raw: str) -> int:
    graph = nx.Graph()
    for line in utils.Input(raw).lines().strings:
        from_node, rest = line.split(":")
        to_nodes = rest.split()
        for node in to_nodes:
            graph.add_edge(from_node, node)

    # Monte Carlo: choose two nodes and find the shortest path between them, then
    # count the edges in that path. Each sample has approx a 50% chance of picking
    # nodes in each side of the network.
    # Remove the most common edge, then repeat two more times. This has a fairly
    # good chance of finding the 3 cuts required, but isn't deterministic.
    # It runs in under 1 second whereas the min edge cut above takes 2.5s.
    nodes = sorted(graph.nodes)
    for edge_cut in range(3):
        seen = Counter()
        for sample in range(20):
            from_node, to_node = random.sample(nodes, 2)
            path = nx.dijkstra_path(graph, from_node, to_node)
            for fnode, tnode in zip(path, path[1:]):
                seen[tuple(sorted((fnode, tnode)))] += 1
        most_seen = seen.most_common(1)[0][0]
        graph.remove_edges_from([most_seen])
    return math.prod(map(len, nx.connected_components(graph)))


def test():
    test_input = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
    answer_1 = part_one_alt(test_input)
    assert answer_1 == 54, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=25, year=2023)
    print("Part 1: ", part_one_alt(data))
