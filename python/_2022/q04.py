import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """Find pairs that fully overlap"""
        pairs = input.split().parse("{:d}-{:d},{:d}-{:d}")
        return sum(
            lmin <= rmin <= rmax <= lmax or rmin <= lmin <= lmax <= rmax
            for lmin, lmax, rmin, rmax in pairs
        )

    def part_two(self, input: utils.Input) -> str | int:
        """Find pairs that partially overlap"""
        pairs = input.split().parse("{:d}-{:d},{:d}-{:d}")
        return sum(
            bool(set(range(lmin, lmax + 1)).intersection(set(range(rmin, rmax + 1))))
            for lmin, lmax, rmin, rmax in pairs
        )


puzzle = Puzzle(
    year=2022,
    day=4,
    test_answers=("2", "4"),
    test_input="""\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""",
)

if __name__ == "__main__":
    puzzle.cli()
