from collections import Counter, defaultdict

import aocd


def part_one(data: list[str]) -> int:
    counter = Counter()
    epsilon = []
    gamma = []
    for column in range(len(data[0])):
        counter = Counter()
        for row in data:
            counter[row[column]] += 1
        common = counter.most_common(2)
        gamma.append(common[0][0])
        epsilon.append(common[1][0])
    return int("".join(gamma), 2) * int("".join(epsilon), 2)


def part_two(data: list[str]) -> int:
    oxygen_options = data
    scrubber_options = data
    oxygen_value = 0
    scrubber_value = 0
    for column in range(len(data[0])):
        oxygen_partition = defaultdict(list)
        scrubber_parition = defaultdict(list)
        for row in oxygen_options:
            oxygen_partition[row[column]].append(row)
        for row in scrubber_options:
            scrubber_parition[row[column]].append(row)

        p0, p1 = oxygen_partition["0"], oxygen_partition["1"]
        if len(p0) <= len(p1):
            oxygen_options = p1
        else:
            oxygen_options = p0

        p0, p1 = scrubber_parition["0"], scrubber_parition["1"]
        if len(p0) <= len(p1):
            scrubber_options = p0
        else:
            scrubber_options = p1

        if len(oxygen_options) == 1:
            oxygen_value = int("".join(oxygen_options[0]), 2)
        if len(scrubber_options) == 1:
            scrubber_value = int("".join(scrubber_options[0]), 2)

    return oxygen_value * scrubber_value


def test():
    test_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
    answer_1 = part_one(test_input.splitlines())
    answer_2 = part_two(test_input.splitlines())
    assert answer_1 == 198, answer_1
    assert answer_2 == 230, answer_2


if __name__ == "__main__":
    test()

    data = aocd.get_data(day=3, year=2021).splitlines()
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
