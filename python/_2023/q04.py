from collections import defaultdict

import aocd

import utils


def part_one(raw: str) -> int:
    data = utils.Input(raw).lines().strings
    # line = Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    total = 0
    for line in data:
        winning_str, ours_str = line.split(":")[1].split("|")
        winning = {int(num) for num in winning_str.split()}
        ours = {int(num) for num in ours_str.split()}
        matched = winning & ours
        if matched:
            total += 2 ** (len(matched) - 1)
    return total


def part_two(raw: str) -> int:
    data = utils.Input(raw).lines().strings
    # line = Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    counter = defaultdict(lambda: 1)
    total = 0
    for line in data:
        card_str, game_str = line.split(":")
        card_num = int(card_str.split()[1])
        winning_str, ours_str = game_str.split("|")
        winning = {int(num) for num in winning_str.split()}
        ours = {int(num) for num in ours_str.split()}
        matched = winning & ours
        for num, _ in enumerate(matched, start=card_num + 1):
            counter[num] += counter[card_num]
        total += counter[card_num]
    return total


def test():
    test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 13, answer_1
    assert answer_2 == 30, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=4, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
