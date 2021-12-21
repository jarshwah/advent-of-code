from __future__ import annotations

import itertools
from collections import Counter
from functools import cache

import aocd


def part_one(data: str) -> int:
    p1, p2 = [int(line[-1]) for line in data.splitlines()]
    dice = range(1, 100000, 3)
    players = [[p1, 0], [p2, 0]]
    for n in dice:
        roll = n * 3 + 3
        position, score = players[0]
        position = position + roll
        while position > 10:
            position -= 10
        score += position
        players[0] = [position, score]
        if score >= 1000:
            return players[1][1] * (n + 2)
        players = list(reversed(players))
    return 1


@cache
def play(p1, s1, p2, s2) -> tuple[int, int]:
    w1, w2 = 0, 0
    counter = Counter([sum(roll) for roll in itertools.product([1, 2, 3], repeat=3)])
    for roll, count in counter.items():
        np1 = p1 + roll
        while np1 > 10:
            np1 -= 10
        ns1 = s1 + np1
        if ns1 >= 21:
            w1 += count
        else:
            # alternate player by switching positions
            nw2, nw1 = play(p2, s2, np1, ns1)
            w1 += nw1 * count
            w2 += nw2 * count
    return w1, w2


def part_two(data: str) -> int:
    p1, p2 = [int(line[-1]) for line in data.splitlines()]
    w1, w2 = play(p1, 0, p2, 0)
    return max(w1, w2)


def test():
    test_input = """Player 1 starting position: 4
Player 2 starting position: 8"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 739785, answer_1
    assert answer_2 == 444356092776315, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=21, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
