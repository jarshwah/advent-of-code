import typing as t
from collections import deque

import aocd
import utils
from utils import DOWN, DOWNLEFT, DOWNRIGHT, LEFT, RIGHT, UP, UPLEFT, UPRIGHT, Point


def solve(raw: str) -> tuple[int, int]:
    grid = utils.Grid(rows=[[]])
    considerations = deque(
        [
            (UPLEFT, UP, UPRIGHT),
            (DOWNLEFT, DOWN, DOWNRIGHT),
            (UPLEFT, LEFT, DOWNLEFT),
            (UPRIGHT, RIGHT, DOWNRIGHT),
        ]
    )
    for row_num, line in enumerate(raw.splitlines()):
        for col_num, tile in enumerate(line):
            if tile == "#":
                grid[row_num, col_num] = "#"
    size_at_10 = 0
    for step in range(100000):
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
        dupes: set[Point] = set()
        for elf in grid:
            diag = list(grid.get_neighbours(elf, diag=True))
            if not diag:
                # No neighbours, stay put
                continue
            found = False
            for consider in considerations:
                if found:
                    break
                nbs = utils.neighbours(elf, directions=consider)
                if any(nb in grid for nb in nbs):
                    # Clash, keep checking
                    continue
                # We move to the middle neighbour
                move_to = nbs[1]
                # dupe, we can't move there and won't consider any others
                if move_to in suggestions:
                    dupes.add(move_to)
                    break
                suggestions[move_to] = elf
                found = True
                break
        # Cancel duplicates
        for dupe in dupes:
            suggestions.pop(dupe, None)
        # Now move them
        for new_pos, old_pos in suggestions.items():
            grid[new_pos] = grid.points.pop(old_pos)

        considerations.append(considerations.popleft())
        if not suggestions:
            return size_at_10, step + 1

    raise ValueError(f"{step=} {size_at_10=}")


def test():
    test_input = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
    answer_1, answer_2 = solve(test_input)
    assert answer_1 == 110, answer_1
    assert answer_2 == 20, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=23, year=2022)
    answer_1, answer_2 = solve(data)
    print("Part 1: ", answer_1)
    print("Part 2: ", answer_2)
