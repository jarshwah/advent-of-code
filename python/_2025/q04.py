from collections import deque
from collections.abc import Sequence

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        grid = input.grid()
        found = list(grid.search(point_accessible, diagonal=True))
        return len(found)

    def part_two(self, input: utils.Input) -> str | int:
        # Brute force - scan top to bottom each time: 6s
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

    def part_two_alt(self, input: utils.Input) -> str | int:
        # Maintain a queue of neighbours that should be rechecked: 0.3s
        grid = input.replace(".", " ").grid()
        removed: set[utils.Point] = set()

        animate = self.animate
        with grid.animate(animate) as animator:
            # we know these are removable, but for the sake of simplicity, we're going to check them all again.
            queue = deque([cand[0] for cand in grid.search(point_accessible, diagonal=True)])
            while queue:
                candidate = queue.popleft()
                if candidate in removed:
                    continue

                # rather than scan top to bottom, just add neighbours of removable to the queue
                neighbours = [nb for nb in grid.neighbours(candidate, diag=True) if grid[nb] == "@"]
                if len(neighbours) < 4:
                    grid[candidate] = " "
                    removed.add(candidate)
                    queue.extend(neighbours)
                    animator.update(grid, header=f"Removed: {len(removed)}")

        return len(removed)


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
