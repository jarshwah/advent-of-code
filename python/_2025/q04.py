from collections.abc import Sequence

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid()
        found = list(grid.search(point_accessible, diagonal=True))
        return len(found)

    def part_two(self, input: utils.Input) -> str | int:
        grid = input.replace(".", " ").grid()
        removed = 0
        loop = 0
        animate = self.animate
        with grid.animate(animate) as animator:
            while True:
                loop += 1
                found = list(grid.search(point_accessible, diagonal=True))
                if not found:
                    break
                for f in found:
                    grid[f[0]] = " "
                    removed += 1
                    animator.update(grid, header=f"Loop: {loop} | Removed: {removed}")
        return removed


def point_accessible(
    candidate: tuple[utils.Point, str], neighbours: Sequence[tuple[utils.Point, str]]
) -> bool:
    if candidate[1] != "@":
        return False
    return sum(1 for nb in neighbours if nb[1] == "@") < 4


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=4,
        test_answers=("13", "43"),
        test_input="""..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""",
    )
    runner.cli()
