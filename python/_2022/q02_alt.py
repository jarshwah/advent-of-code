import enum

import aocd
import utils


class Shape(enum.IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Choice(enum.Enum):
    A = Shape.Rock
    B = Shape.Paper
    C = Shape.Scissors
    X = Shape.Rock
    Y = Shape.Paper
    Z = Shape.Scissors


class Result(enum.IntEnum):
    Lose = 0
    Draw = 3
    Win = 6


class Target(enum.Enum):
    X = Result.Lose
    Y = Result.Draw
    Z = Result.Win


def rock_paper_scissors(them: Shape, us: Shape) -> Result:
    # fmt: off
    match (them, us):
        case (them_shape, us_shape) if them_shape == us_shape: return Result.Draw
        case (Shape.Rock, Shape.Paper) | (Shape.Paper, Shape.Scissors) | (Shape.Scissors, Shape.Rock): return Result.Win
        case _: return Result.Lose
    # fmt: on


def shape_required(them: Shape, us: Result) -> Shape:
    # fmt: off
    match (them, us):
        case (Shape.Rock, Result.Win): return Shape.Paper
        case (Shape.Paper, Result.Win): return Shape.Scissors
        case (Shape.Scissors, Result.Win): return Shape.Rock
        case (Shape.Rock, Result.Lose): return Shape.Scissors
        case (Shape.Paper, Result.Lose): return Shape.Rock
        case (Shape.Scissors, Result.Lose): return Shape.Paper
        case (_, Result.Draw): return them
    # fmt: on


def part_one(raw: str) -> int:
    games = [
        (Choice[abc].value, Choice[xyz].value) for abc, xyz in utils.Input(raw).group("\n").strings
    ]
    return sum(rock_paper_scissors(them, us) + us for them, us in games)


def part_two(raw: str) -> int:
    games = (
        (Choice[abc].value, Target[xyz].value) for abc, xyz in utils.Input(raw).group("\n").strings
    )
    return sum(shape_required(them, target) + target for them, target in games)


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
