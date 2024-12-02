import aocd

import utils


def reflections(lines: list[str], diffs_allowed: int = 0) -> int:
    line_count = 0
    for pos in range(len(lines) - 1):
        diffs = 0
        for start, compare in zip(lines[pos + 1 :], lines[pos::-1]):
            diffs += sum(1 if sx != cx else 0 for sx, cx in zip(start, compare))
        if diffs == diffs_allowed:
            line_count += pos + 1
    return line_count


def part_one(raw: str) -> int:
    valleys = utils.Input(raw).group("\n\n", sep="\n").strings
    total = 0
    for valley in valleys:
        row_wise = [row for row in valley]
        col_wise = [col for col in utils.transpose(valley)]
        total += reflections(row_wise, diffs_allowed=0) * 100
        total += reflections(col_wise, diffs_allowed=0)
    return total


def part_two(raw: str) -> int:
    valleys = utils.Input(raw).group("\n\n", sep="\n").strings
    total = 0
    for valley in valleys:
        row_wise = [row for row in valley]
        col_wise = [col for col in utils.transpose(valley)]
        total += reflections(row_wise, diffs_allowed=1) * 100
        total += reflections(col_wise, diffs_allowed=1)
    return total


def test():
    test_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 405, answer_1
    assert answer_2 == 400, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=13, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
