from __future__ import annotations

import itertools
import re
from dataclasses import dataclass

import aocd
import networkx as nx
import utils

re_valves = re.compile(r"([A-Z]{2})")
re_rate = re.compile(r"rate=(\d+)")


@dataclass(eq=True, frozen=True)
class Frame:
    valve: str
    opened: frozenset[str]
    pressure: int
    time: int

    def __eq__(self, other: Frame):
        return self.pressure == other.pressure

    def __lt__(self, other: Frame):
        return self.pressure < other.pressure


def solve(raw: str, minutes: int, actors: int) -> int:
    # Form a graph, and calculate the path/cost from going from all nodes with
    # a useful valve to all other nodes with a useful valve, plus AA to each of
    # them.
    # Then we iterate through all possibilities going from USEFUL -> USEFUL rather
    # than branching at each possible destination.
    start = "AA"
    useful: dict[str, int] = {}
    graph = nx.Graph()
    for line in utils.Input(raw).lines().strings:
        valves = re_valves.findall(line)
        rate = int(re_rate.search(line)[1])
        curr_valve = valves[0]
        dest_valves = valves[1:]
        if rate > 0:
            useful[curr_valve] = rate
        for dest in dest_valves:
            graph.add_edge(curr_valve, dest)

    # Compute all useful paths
    lengths: dict[frozenset[str], int] = {}
    for u1, u2 in itertools.combinations(useful, 2):
        length = nx.shortest_path_length(graph, u1, u2)
        lengths[frozenset((u1, u2))] = length
    for u1 in useful:
        length = nx.shortest_path_length(graph, start, u1)
        lengths[frozenset((start, u1))] = length

    finished: set[Frame] = set()
    # (valve, visited) = (pressure, time)
    best: dict[tuple[str, frozenset[str], int], int] = {}
    queue = [Frame(start, frozenset(), 0, 1)]
    while queue:
        frame = queue.pop()
        if len(frame.opened) >= 3:
            finished.add(frame)

        # Prune same paths where the time and pressure is lower
        lookup = (frame.valve, frame.opened)
        found = best.get(lookup)
        if found and found[0] >= frame.pressure and found[1] <= frame.time:
            continue
        best[lookup] = (frame.pressure, frame.time)

        try_next = []
        for path, rate in useful.items():
            if path in frame.opened:
                continue

            cost = lengths[frozenset((frame.valve, path))]
            dest_time = frame.time + cost + 1
            if dest_time <= minutes:
                try_next.append(
                    Frame(
                        path,
                        frame.opened | {path},
                        frame.pressure + (rate * (minutes - dest_time + 1)),
                        dest_time,
                    )
                )
        queue.extend(try_next)

    ordered = sorted(finished, key=lambda f: f.pressure, reverse=True)
    if actors == 1:
        return ordered[0].pressure

    if actors == 2:
        optimal = 0
        # Answer is within top 1500, don't look at them all
        check = ((p1, p2) for p1 in ordered[:1500] for p2 in ordered[1:1500] if p1 != p2)
        for p1, p2 in check:
            if p1.opened.isdisjoint(p2.opened):
                optimal = max(optimal, p1.pressure + p2.pressure)
        return optimal

    raise ValueError(actors)


def test():
    test_input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
    answer_1 = solve(test_input, 30, 1)
    answer_2 = solve(test_input, 26, 2)
    assert answer_1 == 1651, answer_1
    assert answer_2 == 1707, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=16, year=2022)
    print("Part 1: ", solve(data, 30, 1))
    print("Part 2: ", solve(data, 26, 2))
