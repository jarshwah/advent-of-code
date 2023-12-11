import itertools

import aocd

import utils


def expand_map(rows: list[str]) -> list[str]:
    non_empty_cols = set()
    non_empty_rows = set()
    num_cols = len(rows[0])
    for rn, row in enumerate(rows):
        for cn, col in enumerate(row):
            if col == "#":
                non_empty_cols.add(cn)
                non_empty_rows.add(rn)
    new_rows = []
    added_rows = 0
    for rn, row in enumerate(rows):
        added_cols = 0
        row_chars = list(row)
        for new_cn in range(num_cols):
            if new_cn not in non_empty_cols:
                row_chars.insert(new_cn + added_cols, ".")
                added_cols += 1
        new_rows.append("".join(row_chars))
        if rn not in non_empty_rows:
            new_rows.insert(rn + added_rows, ["."] * (num_cols + added_cols))
            added_rows += 1
    return new_rows


def part_one(raw: str) -> int:
    rows = expand_map(utils.Input(raw).lines().strings)
    grid = utils.Grid(rows)
    galaxies = (point for point in grid.points if grid[point] == "#")
    combinations = itertools.combinations(galaxies, 2)
    paths = []
    for pair in combinations:
        paths.append((utils.manhattan(*pair), pair))
    breakpoint(context=10)
    return sum(path[0] for path in paths)


def manhattan(
    p1: utils.Point,
    p2: utils.Point,
) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2, strict=True))  # type: ignore


def part_two(raw: str, expand: int) -> int:
    rows = utils.Input(raw).lines().strings
    non_empty_cols = set()
    non_empty_rows = set()
    for rn, row in enumerate(rows):
        for cn, col in enumerate(row):
            if col == "#":
                non_empty_cols.add(cn)
                non_empty_rows.add(rn)
    grid = utils.Grid(rows)
    galaxies = (point for point in grid.points if grid[point] == "#")
    combinations = itertools.combinations(galaxies, 2)
    num_steps = 0
    for pair in combinations:
        steps = 0
        p1, p2 = pair
        start_rn = min(p1[0], p2[0])
        start_cn = min(p1[1], p2[1])
        row_count, col_count = [abs(a - b) for a, b in zip(p1, p2, strict=True)]
        # print(f"{p1=} {p2=} {start_rn=} {start_cn=} {row_count=} {col_count=}")
        for rn in range(start_rn + 1, start_rn + row_count + 1):
            if rn not in non_empty_rows:
                # print(f"{p1[0]=} {p2[0]=} {rn=} {expand=}")
                steps += expand
            else:
                # print(f"{p1[0]=} {p2[0]=} {rn=} 1")
                steps += 1
        for cn in range(start_cn + 1, start_cn + col_count + 1):
            if cn not in non_empty_cols:
                # print(f"{p1[1]=} {p2[1]=} {cn=} {expand=}")
                steps += expand
            else:
                # print(f"{p1[1]=} {p2[1]=} {cn=} 1")
                steps += 1
        num_steps += steps
    return num_steps


def test():
    test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    # answer_1 = part_one(test_input)
    answer_2 = part_two(test_input, expand=10)
    # assert answer_1 == 374, answer_1
    assert answer_2 == 1030, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=11, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data, expand=1000000))
