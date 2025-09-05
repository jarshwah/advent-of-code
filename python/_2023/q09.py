import itertools
from collections.abc import Iterable

import utils


def differences(numbers: list[int]) -> Iterable[int]:
    for i in range(len(numbers) - 1):
        yield numbers[i + 1] - numbers[i]


def add_placeholders(stack: list[list[int]]) -> None:
    stack[-1].append(0)
    for curr, prev in itertools.pairwise(stack[::-1]):
        prev.append(prev[-1] + curr[-1])
        prev.insert(0, prev[0] - curr[0])


class Puzzle(utils.Puzzle):
    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        data = input.group("\n").integers
        extrapolated_right = []
        extrapolated_left = []
        for numbers in data:
            stack = [numbers]
            while not all(num == 0 for num in numbers):
                numbers = list(differences(numbers))
                stack.append(numbers)
            add_placeholders(stack)
            extrapolated_right.append(stack[0][-1])
            extrapolated_left.append(stack[0][0])
        return sum(extrapolated_right), sum(extrapolated_left)


puzzle = Puzzle(
    year=2023,
    day=9,
    test_answers=("114", "2"),
    test_input="""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""",
    both=True,
)

if __name__ == "__main__":
    puzzle.cli()
