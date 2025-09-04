from collections import deque

import utils
from utils import (
    DOWN,
    DOWNLEFT,
    DOWNRIGHT,
    LEFT,
    RIGHT,
    UP,
    UPLEFT,
    UPRIGHT,
    Point,
    neighbours,
)


def solve(raw: str) -> tuple[int, int]:
    grid: set[Point] = set()
    directions8 = [
        UPLEFT,
        UP,
        UPRIGHT,
        RIGHT,
        DOWNRIGHT,
        DOWN,
        DOWNLEFT,
        LEFT,
    ]
    considerations = deque(
        [
            (0, 1, 2),  # UPLEFT, UP, UPRIGHT
            (4, 5, 6),  # DOWNRIGHT, DOWN, DOWNLEFT
            (6, 7, 0),  # DOWNLEFT, LEFT, UPLEFT
            (2, 3, 4),  # UPRIGHT, RIGHT, DOWNRIGHT
        ]
    )

    for row_num, line in enumerate(raw.splitlines()):
        for col_num, tile in enumerate(line):
            if tile == "#":
                grid.add((row_num, col_num))
    size_at_10 = 0
    for step in range(2000):
        if step == 10:
            minr = min(elf[0] for elf in grid)
            maxr = max(elf[0] for elf in grid)
            minc = min(elf[1] for elf in grid)
            maxc = max(elf[1] for elf in grid)
            height = maxr + 1 - minr
            width = maxc + 1 - minc
            size_at_10 = (height * width) - len(grid)
        # to_point: from_point
        suggestions: dict[Point, Point] = {}
        for elf in grid:
            surrounded = neighbours(elf, directions8)
            if set(surrounded).isdisjoint(grid):
                # No Neighbours, stay put
                continue
            for consider in considerations:
                nbs = {surrounded[nb] for nb in consider}
                if not nbs.isdisjoint(grid):
                    # clash, keep checking
                    continue
                move_to = surrounded[consider[1]]
                if move_to in suggestions:
                    # dupe, we can't move there and won't consider any others
                    suggestions.pop(move_to)
                    break
                suggestions[move_to] = elf
                break
        # Now move them
        for new_pos, old_pos in suggestions.items():
            grid.discard(old_pos)
            grid.add(new_pos)

        considerations.append(considerations.popleft())
        if not suggestions:
            return size_at_10, step + 1

    raise ValueError(f"{step=} {size_at_10=}")


class Puzzle(utils.Puzzle):
    pass


puzzle = Puzzle(
    year=2022,
    day=23,
    test_answers=("", ""),
    test_input="""\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..""",
)

if __name__ == "__main__":
    puzzle.cli()
