import operator
from collections import deque
from collections.abc import Callable, Sequence

import utils


def concat(left: int, right: int) -> int:
    return int(str(left) + str(right))


class Puzzle(utils.Puzzle):
    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        """
        Sum together the valid equations.

        A valid equation uses either ADD or MUL to combine the numbers on the right to match
        the number on the left.

        Operators are applied left to right rather than via precedence.

        Part 2 additionally includes the CONCAT operator and is a superset of Part 1.
        """
        p1 = p2 = 0
        for sr, se in input.group("\n", ":").strings:
            check = int(sr)
            values = list(map(int, se.split()))
            if check_equation(check, values, operator.add, operator.mul):
                p1 += check
            elif check_equation(check, values, operator.add, operator.mul, concat):
                p2 += check
        return p1, p2 + p1


def check_equation(check: int, values: Sequence[int], *ops: Callable[[int, int], int]) -> int:
    """
    Sum together the valid equations.

    A valid equation uses either ADD or MUL or CONCAT to combine the numbers on the right to match
    the number on the left.

    Operators are applied left to right rather than via precedence.
    """
    queue = deque([(values[0], values[1:])])
    while queue:
        result, values = queue.popleft()
        if not values:
            if result == check:
                return result
            continue
        queue.extendleft((op(result, values[0]), values[1:]) for op in ops)
    return 0


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=7,
        both=True,
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
