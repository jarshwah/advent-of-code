import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        valleys = utils.Input.group("\n\n", sep="\n").strings
        total = 0
        for valley in valleys:
            row_wise = [row for row in valley]
            col_wise = [col for col in utils.transpose(valley)]
            total += reflections(row_wise, diffs_allowed=0) * 100
            total += reflections(col_wise, diffs_allowed=0)
        return total

    def part_two(self, input: utils.Input) -> str | int:
        valleys = utils.Input.group("\n\n", sep="\n").strings
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
