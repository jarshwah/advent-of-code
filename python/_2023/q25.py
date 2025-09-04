import math
import random
from collections import Counter
import networkx as nx
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        graph = nx.Graph()
        for line in input.lines().strings:
            from_node, rest = line.split(":")
            to_nodes = rest.split()
            for node in to_nodes:
                graph.add_edge(from_node, node)
        graph.remove_edges_from(nx.minimum_edge_cut(graph))
        return math.prod(map(len, nx.connected_components(graph)))


puzzle = Puzzle(
    year=2023,
    day=25,
    test_answers=("", ""),
    test_input="""\
jqt: rhn xhk nvd
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
frs: qnr lhk lsr""",
)

if __name__ == "__main__":
    puzzle.cli()
