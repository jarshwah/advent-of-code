import math

import aocd
import networkx as nx

import utils


def part_one(raw: str) -> int:
    graph = nx.Graph()
    for line in utils.Input(raw).lines().strings:
        try:
            from_node, rest = line.split(":")
        except Exception:
            breakpoint(context=10)
        to_nodes = rest.split()
        for node in to_nodes:
            graph.add_edge(from_node, node)
    graph.remove_edges_from(nx.minimum_edge_cut(graph))
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
    answer_1 = part_one(test_input)
    assert answer_1 == 54, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=25, year=2023)
    print("Part 1: ", part_one(data))
