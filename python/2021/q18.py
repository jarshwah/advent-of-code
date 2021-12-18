import itertools
import math
from ast import literal_eval
from typing import Optional, Union

import aocd

Expr = Union[list, int]
MaybeInt = Optional[int]


def magnitude(expression: Expr) -> int:
    if isinstance(expression, int):
        return expression
    left, right = expression
    return 3 * magnitude(left) + 2 * magnitude(right)


def add_left(expression: Expr, value: MaybeInt) -> Expr:
    if value is None:
        return expression
    if isinstance(expression, int):
        return expression + value
    return [add_left(expression[0], value), expression[1]]


def add_right(expression: Expr, value: MaybeInt) -> Expr:
    if value is None:
        return expression
    if isinstance(expression, int):
        return expression + value
    return [expression[0], add_right(expression[1], value)]


def explode(expression: Expr, depth: int = 0) -> tuple[Expr, bool, MaybeInt, MaybeInt]:
    if isinstance(expression, int):
        return expression, False, None, None

    left, right = expression
    if depth == 4:
        return 0, True, left, right

    left, changed, new_left, new_right = explode(left, depth=depth + 1)
    if changed:
        # left-most value to the right is mutated
        return [left, add_left(right, new_right)], changed, new_left, None

    right, changed, new_left, new_right = explode(right, depth=depth + 1)
    if changed:
        # right-most value to the left is mutated
        return [add_right(left, new_left), right], changed, None, new_right

    return expression, False, None, None


def split(expression: Expr) -> tuple[Expr, bool]:
    if isinstance(expression, int):
        if expression >= 10:
            left = expression // 2
            right = int(math.ceil(expression / 2))
            return [left, right], True
        return expression, False
    left, right = expression
    left, changed = split(left)
    if changed:
        return [left, right], changed
    right, changed = split(right)
    return [left, right], changed


def reduce_expression(expression) -> list:
    expression, did_explode, _, _ = explode(expression, depth=0)
    if did_explode:
        return reduce_expression(expression)
    expression, did_split = split(expression)
    if did_split:
        return reduce_expression(expression)
    return expression


def add(lexpression, rexpression) -> list:
    return [lexpression, rexpression]


def sums(expressions: list[Expr]) -> Expr:
    left = expressions[0]
    for next_expression in expressions[1:]:
        left = reduce_expression(add(left, next_expression))
    return left


def part_one(data: str) -> int:
    expressions = [literal_eval(expr) for expr in data.splitlines()]
    return magnitude(sums(expressions))


def part_two(data: str) -> int:
    expressions = [literal_eval(expr) for expr in data.splitlines()]
    pairs = list(itertools.permutations(expressions, 2))
    return max(magnitude(sums(pair)) for pair in pairs)


def test():
    m1 = magnitude([[1, 2], [[3, 4], 5]])
    assert m1 == 143, m1
    m2 = magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])
    assert m2 == 3488, m2
    e1, changed, _, _ = explode([[[[[9, 8], 1], 2], 3], 4])
    assert (e1, changed) == ([[[[0, 9], 2], 3], 4], True), e1
    e2, changed, _, _ = explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    assert (e2, changed) == ([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], True), e2

    s1, changed = split([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
    assert s1 == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]], s1

    test_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 4140, answer_1
    assert answer_2 == 3993, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=18, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
