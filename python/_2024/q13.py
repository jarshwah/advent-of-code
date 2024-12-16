from collections.abc import Sequence

import z3

import utils


def how_many_tokens(game: Sequence[Sequence[int]], scale: int) -> int:
    """
    Fewest tokens needed to win all possible prizes.

    Scale PX and PY by 10000000000000 and remove the max 100 press constraint.
    """
    AX, AY, BX, BY, PX, PY = utils.flatten(game)
    solver = z3.Optimize()
    ZA, ZB = z3.Ints("ZA ZB")
    solver.add(
        ZA * AX + ZB * BX == PX + scale,
        ZA * AY + ZB * BY == PY + scale,
    )
    if solver.check() == z3.sat:
        model = solver.model()
        return int(model[ZA].as_long()) * 3 + int(model[ZB].as_long())
    return 0


class Puzzle(utils.Puzzle):
    """
    A button: 3 tokens
    B button: 1 token

    Buttons move RIGHT (x axis) and FORWARD (y axis).
    Machine contains 1 prize. Claw must be positioned exactly over the prize.
    Each machines buttons have different RIGHT AND FORWARD values.

    Smallest number of tokens needed to win as many prizes as possible.
    """

    def part_one(self, input: utils.Input) -> str | int:
        """
        Fewest tokens needed to win all possible prizes.
        """
        games = input.group("\n\n", "\n").scan_ints()
        return sum(how_many_tokens(game, scale=0) for game in games)

    def part_two(self, input: utils.Input) -> str | int:
        """
        Fewest tokens needed to win all possible prizes.

        Scale PX and PY by 10000000000000.
        """
        games = input.group("\n\n", "\n").scan_ints()
        return sum(how_many_tokens(game, scale=10000000000000) for game in games)


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=13,
        test_answers=("480", "875318608908"),
        test_input="""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""",
    )
    runner.cli()
