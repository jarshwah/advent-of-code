import math

import aocd

import utils


def part_one(raw: str) -> int:
    games = zip(
        *[[int(n) for n in s.split(":")[1].split()] for s in utils.Input(raw).lines().strings]
    )
    game_wins = []
    for time, record in games:
        wins = 0
        for attempt in range(1, time):
            would_be = attempt * (time - attempt)
            if would_be > record:
                wins += 1
        game_wins.append(wins)
    return math.prod(game_wins)


def part_two(raw: str) -> int:
    time_s, distance_s = utils.Input(raw).lines().strings
    time = int(time_s.split(":")[1].replace(" ", ""))
    distance = int(distance_s.split(":")[1].replace(" ", ""))
    wins = 0
    for attempt in range(1, time):
        would_be = attempt * (time - attempt)
        if would_be > distance:
            wins += 1
    return wins


def test():
    test_input = """Time:      7  15   30
Distance:  9  40  200"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 288, answer_1
    assert answer_2 == 71503, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=6, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
