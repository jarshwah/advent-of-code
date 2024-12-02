import aocd

import utils


def part_one(raw: str) -> int:
    games = zip(
        *[[int(n) for n in s.split(":")[1].split()] for s in utils.Input(raw).lines().strings]
    )
    game_wins = 1
    for time, record in games:
        wins = 0
        for attempt in range(1, time):
            would_be = attempt * (time - attempt)
            if would_be > record:
                wins += 1
        game_wins *= wins
    return game_wins


def part_two(raw: str) -> int:
    time, distance = [
        int(s.split(":")[1].replace(" ", "")) for s in utils.Input(raw).lines().strings
    ]
    return sum(1 for attempt in range(1, time) if attempt * (time - attempt) > distance)


def part_two_alt(raw: str) -> int:
    # Halve the search space - check from the midpoint and return when we exceed
    # the distance, doubling the result.
    time, distance = [
        int(s.split(":")[1].replace(" ", "")) for s in utils.Input(raw).lines().strings
    ]
    for idx, attempt in enumerate(range(time // 2, time)):
        if attempt * (time - attempt) <= distance:
            return idx * 2 - 1


def test():
    test_input = """Time:      7  15   30
Distance:  9  40  200"""
    answer_1 = part_one(test_input)
    answer_2 = part_two_alt(test_input)
    assert answer_1 == 288, answer_1
    assert answer_2 == 71503, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=6, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two_alt(data))
