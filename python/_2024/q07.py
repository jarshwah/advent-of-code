import itertools
import operator
from collections.abc import Callable, Sequence

import utils


def concat(left: int, right: int) -> int:
    return int(str(left) + str(right))


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Sum together the valid equations.

        A valid equation uses either ADD or MUL to combine the numbers on the right to match
        the number on the left.

        Operators are applied left to right rather than via precedence.
        """
        summed = 0
        for sr, se in input.group("\n", ":").strings:
            check = int(sr)
            values = list(map(int, se.split()))
            summed += check_equation(check, values, operator.add, operator.mul)
        return summed

    def part_two(self, input: utils.Input) -> str | int:
        summed = 0
        for sr, se in input.group("\n", ":").strings:
            check = int(sr)
            values = list(map(int, se.split()))
            summed += check_equation(check, values, operator.add, operator.mul, concat)
        return summed


def check_equation(check: int, values: Sequence[int], *ops: Callable[[int, int], int]) -> int:
    """
    Sum together the valid equations.

    A valid equation uses either ADD or MUL or CONCAT to combine the numbers on the right to match
    the number on the left.

    Operators are applied left to right rather than via precedence.
    """
    operations = itertools.product(ops, repeat=len(values) - 1)
    for op_set in operations:
        result = values[0]
        for op, value in zip(op_set, values[1:]):
            result = op(result, value)
            if result > check:
                break
        if result == check:
            return result
    return 0


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=7,
        test_answers=("3749", "11387"),
        test_input="""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""",
    )
    runner.cli()
