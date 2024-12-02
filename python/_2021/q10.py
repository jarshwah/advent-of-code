from functools import reduce
from statistics import median

import aocd

OPEN = "([{<"
CLOSE = ")]}>"
POINTS = [3, 57, 1197, 25137]


def both_parts(lines: str) -> tuple[int, int]:
    a1, a2 = 0, []
    for line in lines:
        stack = []
        for ch in line:
            if ch in OPEN:
                stack.append(ch)
                continue
            if OPEN[CLOSE.index(ch)] != stack.pop():
                a1 += POINTS[CLOSE.index(ch)]
                break
        else:
            a2.append(reduce(lambda cum, item: cum * 5 + OPEN.index(item) + 1, reversed(stack), 0))
    return a1, int(median(sorted(a2)))


def test():
    test_input = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

    answer_1, answer_2 = both_parts(test_input.splitlines())
    assert answer_1 == 26397, answer_1
    assert answer_2 == 288957, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=10, year=2021)
    p1, p2 = both_parts(data.splitlines())
    print("Part 1: ", p1)
    print("Part 2: ", p2)
