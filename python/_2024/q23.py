import networkx as nx

import utils


class Puzzle(utils.Puzzle):
    """
    Input shows all connected computers (non-directed).
    """

    def part_one(self, input: utils.Input) -> str | int:
        """
        Find the number of 3-node connected computers.
        """
        pairs = [line.split("-") for line in input.lines().strings]
        graph = nx.from_edgelist(pairs)
        triples = 0
        cliques = list(nx.enumerate_all_cliques(graph))
        for clique in cliques:
            if len(clique) == 3 and any(c.startswith("t") for c in clique):
                triples += 1
        return triples

    def part_two(self, input: utils.Input) -> str | int:
        """
        Find the largest N-node connected computers.
        """
        pairs = [line.split("-") for line in input.lines().strings]
        graph = nx.from_edgelist(pairs)
        lan_party = max(nx.enumerate_all_cliques(graph), key=len)
        return ",".join(sorted(lan_party))


puzzle = Puzzle(
    year=2024,
    day=23,
    test_answers=("7", "co,de,ka,ta"),
    test_input="""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn""",
)

if __name__ == "__main__":
    puzzle.cli()
