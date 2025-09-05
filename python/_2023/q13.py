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


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        valleys = input.group("\n\n", sep="\n").strings
        total = 0
        for valley in valleys:
            row_wise = [row for row in valley]
            col_wise = [col for col in utils.transpose(valley)]
            total += reflections(row_wise, diffs_allowed=0) * 100
            total += reflections(col_wise, diffs_allowed=0)
        return total

    def part_two(self, input: utils.Input) -> str | int:
        valleys = input.group("\n\n", sep="\n").strings
        total = 0
        for valley in valleys:
            row_wise = [row for row in valley]
            col_wise = [col for col in utils.transpose(valley)]
            total += reflections(row_wise, diffs_allowed=1) * 100
            total += reflections(col_wise, diffs_allowed=1)
        return total


puzzle = Puzzle(
    year=2023,
    day=13,
    test_answers=("405", "400"),
    test_input="""\
#.##..##.
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
#....#..#""",
)

if __name__ == "__main__":
    puzzle.cli()
