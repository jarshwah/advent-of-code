import typing as t
import aocd


table = str.maketrans("FBLR", "0101")


def part_one(passes: t.List[str]) -> int:
    return max(int(bp.translate(table), 2) for bp in passes)


def part_two(passes: t.List[str]) -> int:
    ordered = sorted(int(bp.translate(table), 2) for bp in passes)
    return next(bp + 1 for n, bp in enumerate(ordered) if ordered[n + 1] == bp + 2)


if __name__ == "__main__":
    passes = aocd.get_data(day=5, year=2020).splitlines()
    print("Part 1: ", part_one(passes))
    print("Part 2: ", part_two(passes))
