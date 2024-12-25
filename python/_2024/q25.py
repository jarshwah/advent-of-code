import utils

type Pins = tuple[int, int, int, int, int, int]


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        groups = input.split("\n\n").strings
        keys = set()
        locks = set()
        for group in groups:
            lines = group.splitlines()
            if lines[0] == "#####":
                # locks
                pins = []
                cols = utils.rotate(lines[1:])
                for col in cols:
                    pins.append(col.count("."))
                locks.add(tuple(pins))
            else:
                # keys
                cols = utils.rotate(lines[0:-1])
                pins = []
                for col in cols:
                    pins.append(col.count("#"))
                keys.add(tuple(pins))
        return sum(1 for key in keys for lock in locks if all(ky < lk for ky, lk in zip(key, lock)))

    def part_two(self, input: utils.Input) -> str | int:
        return "no-answer"


if __name__ == "__main__":
    runner = Puzzle(
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
    runner.cli()
