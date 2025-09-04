import itertools

import utils


def compute_expansion(input: utils.Input, expand: int) -> int:
    rows = input.lines().strings
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


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        return compute_expansion(input, expand=2)

    def part_two(self, input: utils.Input) -> str | int:
        # For test mode, use expand=10 instead of 1000000
        expand = 10 if self.testing else 1000000
        return compute_expansion(input, expand=expand)


puzzle = Puzzle(
    year=2023,
    day=11,
    test_answers=("374", "1030"),
    test_input="""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""",
)

if __name__ == "__main__":
    puzzle.cli()
