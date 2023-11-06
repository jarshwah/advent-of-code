from collections import Counter

import aocd


def part_one(data: str) -> int:
    lines = data.splitlines()
    code = lines[0]
    transforms = {s[0]: s[1] for x in lines[2:] if (s := x.split(" -> "))}
    for n in range(10):
        pairs = [f"{x}{y}" for x, y in zip(code, code[1:])]
        new_code = []
        for idx, pair in enumerate(pairs, 1):
            new = transforms[pair]
            if idx == len(pairs):
                new_code.extend([pair[0], new, pair[1]])
            else:
                new_code.extend([pair[0], new])
        code = "".join(new_code)
    c = Counter(code)
    mc = c.most_common()
    return mc[0][1] - mc[-1][1]


def part_two(data: str) -> int:
    lines = data.splitlines()
    code = lines[0]
    transforms = {tuple(s[0]): s[1] for x in lines[2:] if (s := x.split(" -> "))}
    c1 = Counter(zip(code, code[1:]))
    for n in range(40):
        c2 = Counter()
        for pair in c1:
            lpair = pair[0], transforms[pair]
            c2[lpair] += c1[pair]
            rpair = transforms[pair], pair[1]
            c2[rpair] += c1[pair]
        c1 = c2
    c2 = Counter()
    for pair in c1:
        c2[pair[0]] += c1[pair]
    # we missed the very last char only counting the lhs, so add it from
    # the string
    c2[code[-1]] += 1
    mc = c2.most_common()
    ans = mc[0][1] - mc[-1][1]
    return ans


def test():
    test_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 1588, answer_1
    assert answer_2 == 2651311098752, answer_2  # this is wrong, wtf


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=14, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
