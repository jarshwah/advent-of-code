from __future__ import annotations

import itertools
import re
from dataclasses import dataclass

import aocd
import utils

re_valves = re.compile(r"([A-Z]{2})")
re_rate = re.compile(r"rate=(\d+)")


@dataclass(eq=True, frozen=True)
class Frame:
    valve: str
    opened: frozenset[str]
    pressure: int

    def __eq__(self, other: Frame):
        return self.pressure == other.pressure

    def __lt__(self, other: Frame):
        return self.pressure < other.pressure


@dataclass(eq=True, frozen=True)
class Pair:
    valves: tuple[str, str]
    opened: frozenset[str]
    pressure: int

    def __eq__(self, other: Frame):
        return self.pressure == other.pressure

    def __lt__(self, other: Frame):
        return self.pressure < other.pressure


def part_one(raw: str) -> int:
    paths = {}
    already_open = set()
    for line in utils.Input(raw).lines().strings:
        valves = re_valves.findall(line)
        rate = int(re_rate.search(line)[1])
        curr_valve = valves[0]
        dest_valves = valves[1:]
        paths[curr_valve] = (rate, tuple(dest_valves))
        if rate == 0:
            already_open.add(curr_valve)

    # (valve, opened_valves) => pressure
    best: dict[tuple[str, frozenset[str]], int] = {}
    queue = [Frame("AA", frozenset(already_open), 0)]
    for minute in range(30, 0, -1):
        new_queue = []
        for frame in queue:
            lookup = (frame.valve, frame.opened)
            if frame.pressure <= best.get(lookup, -1):
                # We've visited here with higher pressure, abort path
                continue
            best[lookup] = frame.pressure
            rate, dests = paths[frame.valve]
            # Open the valve?
            if frame.valve not in frame.opened:
                new_queue.append(
                    Frame(
                        frame.valve,
                        frame.opened | {frame.valve},
                        frame.pressure + (rate * (minute - 1)),
                    )
                )
            # Move to another valve
            new_queue.extend(Frame(dest, frame.opened, frame.pressure) for dest in dests)
        # recurse
        queue = new_queue
    return max(frame.pressure for frame in queue)


def part_two(raw: str) -> int:
    # TODO:
    # Form a graph, then compute the cost of going from every node to every
    # other node. Exclude nodes with 0 flow, we don't ever want to rest there.
    #
    # Compute all paths and their flow rate under the time limit
    #
    # Then find the max sum of pairs with distinct paths that do not intersect starting
    # from highest to lowest.
    paths = {}
    already_open = set()
    for line in utils.Input(raw).lines().strings:
        valves = re_valves.findall(line)
        rate = int(re_rate.search(line)[1])
        curr_valve = valves[0]
        dest_valves = valves[1:]
        paths[curr_valve] = (rate, tuple(dest_valves))
        if rate == 0:
            already_open.add(curr_valve)


def part_two_too_slow(raw: str) -> int:
    paths = {}
    already_open = set()
    for line in utils.Input(raw).lines().strings:
        valves = re_valves.findall(line)
        rate = int(re_rate.search(line)[1])
        curr_valve = valves[0]
        dest_valves = valves[1:]
        paths[curr_valve] = (rate, tuple(dest_valves))
        if rate == 0:
            already_open.add(curr_valve)

    # ((valves,), opened_valves) => pressure
    best: dict[tuple[tuple[str, str], frozenset[str]], int] = {}
    queue = [Pair(("AA", "AA"), frozenset(already_open), 0)]
    opening_combinations = list(itertools.product((True, False), repeat=2))
    for minute in range(26, 0, -1):
        new_queue = []
        for frame in queue:
            lookup = (frame.valves, frame.opened)
            if frame.pressure <= best.get(lookup, -1):
                # We've visited here with higher pressure, abort path
                print(f"Found at {minute}: {lookup}")
                continue
            best[lookup] = frame.pressure
            opened = frame.opened
            pressure = frame.pressure
            v1, v2 = frame.valves
            same_valve = v1 == v2
            rate1, dests1 = paths[v1]
            rate2, dests2 = paths[v2]

            for open1, open2 in opening_combinations:
                match (open1, open2):
                    case True, True if v1 not in opened and v2 not in opened and not same_valve:
                        new_queue.append(
                            Pair(
                                (v1, v2),
                                opened | {v1, v2},
                                pressure + (rate1 * (minute - 1)) + (rate2 * (minute - 1)),
                            )
                        )

                    case True, False if v1 not in opened:
                        # Only open v1 and traverse v2
                        new_queue.extend(
                            Pair(
                                (v1, dest),
                                opened | {v1},
                                pressure + (rate1 * (minute - 1)),
                            )
                            for dest in dests2
                        )
                    case False, True if v2 not in opened:
                        # Only open v2 and traverse v1
                        new_queue.extend(
                            Pair(
                                (dest, v2),
                                opened | {v2},
                                pressure + (rate2 * (minute - 1)),
                            )
                            for dest in dests1
                        )
                    case False, False:
                        # Open neither, traverse both v1,v2, in all combinations
                        new_queue.extend(
                            Pair((d1, d2), opened, pressure)
                            for d1, d2 in itertools.product(dests1, dests2)
                        )
                    case _:
                        print("Continuing??")
        if not new_queue:
            print(f"No queue {minute}: {max(frame.pressure for frame in queue)}")
        queue = new_queue
    return max(frame.pressure for frame in queue)


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
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 1651, answer_1
    assert answer_2 == 1707, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=16, year=2022)
    print("Part 1: ", part_one(data))
    # print("Part 2: ", part_two(data))
