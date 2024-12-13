import z3

import utils


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

        Max presses per button is 100
        """
        games = input.group("\n\n", "\n").parse(
            "Button {}: X+{x:d}, Y+{y:d}", "Prize: X={x:d}, Y={y:d}"
        )
        ans = 0
        for game_num, (A, B, P) in enumerate(games):
            AX, AY = A["x"], A["y"]
            BX, BY = B["x"], B["y"]
            PX, PY = P["x"], P["y"]
            solver = z3.Optimize()
            ZA = z3.Int("ZA")
            ZB = z3.Int("ZB")
            solver.add(
                (ZA * AX) + (ZB * BX) == PX,
                (ZA * AY) + (ZB * BY) == PY,
                0 <= ZA,
                ZA <= 100,
                0 <= ZB,
                ZB <= 100,
            )
            # solver.minimize(ZA * 3 + ZB)  -> tanks performance, still right answer
            if solver.check() == z3.sat:
                model = solver.model()
                a_presses = model[ZA].as_long()
                b_presses = model[ZB].as_long()
                tokens = a_presses * 3 + b_presses
                ans += tokens

        return ans

    def part_two(self, input: utils.Input) -> str | int:
        """
        Fewest tokens needed to win all possible prizes.

        Scale PX and PY by 10000000000000 and remove the max 100 press constraint.
        """
        games = input.group("\n\n", "\n").parse(
            "Button {}: X+{x:d}, Y+{y:d}", "Prize: X={x:d}, Y={y:d}"
        )
        ans = 0
        for game_num, (A, B, P) in enumerate(games):
            AX, AY = A["x"], A["y"]
            BX, BY = B["x"], B["y"]
            PX, PY = P["x"] + 10000000000000, P["y"] + 10000000000000
            solver = z3.Optimize()
            ZA = z3.Int("ZA")
            ZB = z3.Int("ZB")
            solver.add(
                (ZA * AX) + (ZB * BX) == PX,
                (ZA * AY) + (ZB * BY) == PY,
                0 <= ZA,
                0 <= ZB,
            )
            solver.minimize(ZA * 3 + ZB)
            if solver.check() == z3.sat:
                model = solver.model()
                a_presses = model[ZA].as_long()
                b_presses = model[ZB].as_long()
                tokens = a_presses * 3 + b_presses
                ans += tokens

        return ans


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
