import aocd

import utils


def parse(data: str) -> list[tuple[list[str], list[str]]]:
    rows = []
    for line in data.splitlines():
        L, R = line.split(" | ")
        rows.append((L.strip().split(), R.strip().split()))
    return rows


def part_one(data: str) -> int:
    rows = parse(data)
    total = 0
    for row in rows:
        for display in row[1]:
            if len(display) in {7, 4, 3, 2}:
                total += 1
    return total


def solve(row: tuple[list[str], list[str]]) -> int:
    flashes = row[0]
    d1 = set(utils.only(c for c in flashes if len(c) == 2))
    d4 = set(utils.only(c for c in flashes if len(c) == 4))
    d7 = set(utils.only(c for c in flashes if len(c) == 3))
    d8 = set(utils.only(c for c in flashes if len(c) == 7))
    # 1 has TR which 6 does not but 9 and 0 do
    d6 = set(utils.only(c for c in flashes if len(c) == 6 and d1 - set(c)))
    # 4 has M which 0 does not but 9 has all of 4
    d0 = set(utils.only(c for c in flashes if len(c) == 6 and set(c) != d6 and d4 - set(c)))
    # 9 is length 6 but not 0 or 6
    d9 = set(utils.only(c for c in flashes if len(c) == 6 and set(c) not in [d6, d0]))
    # 5 is length 5 and fully contained within 6
    d5 = set(utils.only(c for c in flashes if len(c) == 5 and not set(c) - d6))
    # 3 is length 5, but not 5, and fully contained within 9
    d3 = set(
        utils.only(c for c in flashes if len(c) == 5 and not set(c) - d9 and not set(c) == d5)
    )
    # 2 is length 5 and not 3 or 5
    d2 = set(utils.only(c for c in flashes if len(c) == 5 and set(c) not in [d3, d5]))

    lookup = [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9]
    num = []
    for digit in row[1]:
        num.append(str(lookup.index(set(digit))))
    return int("".join(num))


def part_two(data: str) -> int:
    rows = parse(data)
    total = 0
    for row in rows:
        total += solve(row)
    return total


def test():
    test_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 26, answer_1
    assert answer_2 == 61229, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=8, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
