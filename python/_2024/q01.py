import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Find the distance between sorted pairs from columns.
        """
        left, right = map(sorted, input.columns().numbers)
        return sum(abs(a - b) for a, b in zip(left, right))

    def part_two(self, input: utils.Input) -> str | int:
        """
        Find the similarity between sorted first column, summing left by the
        count of matches in right.
        """
        left, right = map(sorted, input.columns().numbers)
        return sum(ln * right.count(ln) for ln in left)


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=1,
        test_answers=("11", "31"),
        test_input="""3   4
4   3
2   5
1   3
3   9
3   3""",
    )
    runner.cli()
