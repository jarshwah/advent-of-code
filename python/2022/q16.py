from __future__ import annotations

import re
import typing as t
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


def part_one(raw: str) -> int:
    paths = {}
    for line in utils.Input(raw).lines().strings:
        valves = re_valves.findall(line)
        rate = int(re_rate.search(line)[1])
        curr_valve = valves[0]
        dest_valves = valves[1:]
        paths[curr_valve] = (rate, tuple(dest_valves))

    # (valve, opened_valves) => pressure
    best: dict[tuple(str, frozenset[str]), int] = {}
    queue = [Frame("AA", frozenset(), 0)]
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
            if frame.valve not in frame.opened and rate > 0:
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
    data = utils.Input(raw)
    return 1


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
    assert answer_2 == 1, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=16, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
