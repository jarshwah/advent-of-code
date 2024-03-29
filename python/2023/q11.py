import itertools

import aocd

import utils


def both_parts(raw: str, expand: int) -> int:
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
        p1, p2 = pair
        start_rn = min(p1[0], p2[0])
        start_cn = min(p1[1], p2[1])
        row_count, col_count = [abs(a - b) for a, b in zip(p1, p2, strict=True)]
        for rn in range(start_rn + 1, start_rn + row_count + 1):
            num_steps += 1 if rn in non_empty_rows else expand
        for cn in range(start_cn + 1, start_cn + col_count + 1):
            num_steps += 1 if cn in non_empty_cols else expand
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
    answer_1 = both_parts(test_input, expand=2)
    answer_2 = both_parts(test_input, expand=10)
    assert answer_1 == 374, answer_1
    assert answer_2 == 1030, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=11, year=2023)
    print("Part 1: ", both_parts(data, expand=2))
    print("Part 2: ", both_parts(data, expand=1000000))
