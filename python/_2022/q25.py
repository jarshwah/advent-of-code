import itertools

import aocd

TONUM = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
TOCHAR = {v: k for k, v in TONUM.items()}


def part_one(raw: str) -> str:
    numbers = ["".join(reversed(num)) for num in raw.splitlines()]
    max_cols = max(len(n) for n in numbers)
    answer = [0] * max_cols
    # Add up all of the numbers and carry over what we need
    zipped = itertools.zip_longest(*numbers, fillvalue="0")
    for pos, columns in enumerate(zipped):
        total = sum(TONUM[c] for c in columns) + answer[pos]
        if not (-2 <= total <= 2):
            mults, _ = divmod(total + 2, 5)
            answer[pos + 1] += mults
            total -= 5 * mults
        answer[pos] = total
    return "".join(TOCHAR[a] for a in reversed(answer))


def test():
    test_input = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
    answer_1 = part_one(test_input)
    assert answer_1 == "2=-1=0", answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=25, year=2022)
    print("Part 1: ", part_one(data))
