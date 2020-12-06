import typing as t

import aocd


def part_one(data: t.List[str]) -> int:
    return sum(len(set(rec.replace("\n", ""))) for rec in data)


def part_two(data: t.List[str]) -> int:
    return sum(
        len(set.intersection(*[set(person) for person in group.split("\n")])) for group in data
    )


if __name__ == "__main__":
    data = aocd.get_data(day=6, year=2020).split("\n\n")
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
