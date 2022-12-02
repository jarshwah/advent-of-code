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


def play(oppo: int, us: int) -> int:
    """
    Return the score of playing the game.

    Our score + 6 for a win, 3 for a draw, 0 for a loss
    """
    if oppo == us:  # draw
        return 3 + us
    if (us - oppo) % 3 == 1:  # win
        return 6 + us
    return us  # lose


def play_two(them: int, us: int):
    """
    Return the score of playing the game.

    Us: 2 = draw, 1 = lose, 3 = win
    """
    if us == 2:  # draw
        return 3 + them
    if us == 1:  # lose
        return (them - 1) or 3
    return (1 if them == 3 else them + 1) + 6  # win


def part_one(raw: str) -> int:
    data = utils.Input(raw).group("\n").strings
    score = []
    for opponent, us in data:
        oscore = table[opponent]
        usscore = table[us]
        score.append(play(oscore, usscore))
    return sum(score)


def part_two(raw: str) -> int:
    data = utils.Input(raw).group("\n").strings
    score = []
    for opponent, us in data:
        oscore = table[opponent]
        usscore = table[us]
        score.append(play_two(oscore, usscore))
    return sum(score)


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
