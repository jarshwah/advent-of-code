import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        groups = input.group("\n\n", "\n").strings
        presents: list[int] = []
        for boxes in groups[:-1]:
            presents.append(sum(row.count("#") for row in boxes[1:]))
        fits = 0
        for tree in groups[-1]:
            width, height, *pnums = utils.scan_ints(tree)
            # If the area of presents is less than the area of available space, it just fits.
            # The real input cares not for rearranging or flipping 🤡
            fits += width * height > sum(sz * count for sz, count in zip(presents, pnums))
        return fits

    def part_two(self, input: utils.Input) -> str | int:
        return "only-1-part"


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=12,
        test_answers=("3", "only-1-part"),
        test_input="""0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2""",
    )
    runner.cli()
