import utils

type Pins = tuple[int, int, int, int, int, int]


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        groups = input.split("\n\n").strings
        keys = set()
        locks = set()
        for group in groups:
            lines = group.splitlines()
            cols = utils.rotate(lines)
            slots = tuple(col.count("#") for col in cols)
            locks.add(slots) if cols[0][0].startswith("#") else keys.add(slots)
        height = len(cols[0])
        return sum(
            1
            for key in keys
            for lock in locks
            if all(ky + lk <= height for ky, lk in zip(key, lock))
        )

    def part_two(self, input: utils.Input) -> str | int:
        return "no-answer"


puzzle = Puzzle(
    year=2024,
    day=25,
    test_answers=("3", "no-answer"),
    test_input="""#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####""",
)

if __name__ == "__main__":
    puzzle.cli()
