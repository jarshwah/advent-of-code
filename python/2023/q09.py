from collections.abc import Iterable

import aocd

import utils


def differences(numbers: list[int]) -> Iterable[int]:
    for i in range(len(numbers) - 1):
        yield numbers[i + 1] - numbers[i]


def add_placeholders(stack: list[list[int]]) -> None:
    stack[-1].append(0)
    for i in range(len(stack) - 1, 0, -1):
        stack[i - 1].append(stack[i - 1][-1] + stack[i][-1])
        stack[i - 1].insert(0, stack[i - 1][0] - stack[i][0])


def both_parts(raw: str) -> tuple[int, int]:
    data = utils.Input(raw).group("\n").integers
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


def test():
    test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    answer_1, answer_2 = both_parts(test_input)
    assert answer_1 == 114, answer_1
    assert answer_2 == 2, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=9, year=2023)
    p1, p2 = both_parts(data)
    print("Part 1: ", p1)
    print("Part 2: ", p2)
