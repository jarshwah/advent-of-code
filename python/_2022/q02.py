import aocd
import utils

table = {
    "A": 1,  # rock
    "B": 2,  # paper
    "C": 3,  # scissors
    # -----------------
    "X": 1,  # rock/lose
    "Y": 2,  # paper/draw
    "Z": 3,  # scissors/win
}


def part_one(raw: str) -> int:
    data = utils.Input(raw).group("\n").strings
    score = 0
    for opponent, us in data:
        them, ours = table[opponent], table[us]
        if them == ours:  # draw
            score += 3 + ours
            continue
        elif (ours - them) % 3 == 1:  # win
            score += 6 + ours
            continue
        score += ours  # lose
    return score


def part_two(raw: str) -> int:
    data = utils.Input(raw).group("\n").strings
    score = 0
    for opponent, us in data:
        them, ours = table[opponent], table[us]
        if ours == 2:  # draw
            score += 3 + them
            continue
        elif ours == 1:  # lose
            score += (them - 1) or 3
            continue
        score += (1 if them == 3 else them + 1) + 6  # win
    return score


def test():
    test_input = """A Y
B X
C Z"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 15, answer_1
    assert answer_2 == 12, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=2, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
