import typing as t
from utils import Point
import utils


def horizontal(height) -> set[Point]:
    return {(height, 2), (height, 3), (height, 4), (height, 5)}


def plus(height: int) -> set[Point]:
    return {(height, 3), (height + 1, 2), (height + 1, 3), (height + 1, 4), (height + 2, 3)}


def L(height: int) -> set[Point]:
    return {(height, 2), (height, 3), (height, 4), (height + 1, 4), (height + 2, 4)}


def vertical(height: int) -> set[Point]:
    return {(height, 2), (height + 1, 2), (height + 2, 2), (height + 3, 2)}


def square(height: int) -> set[Point]:
    return {(height, 2), (height + 1, 2), (height, 3), (height + 1, 3)}


def move_sideways(rock: set[Point], direction: SIDEWAYS) -> set[Point]:
    if direction == RIGHT and any(p[1] == 6 for p in rock):
        return rock
    if direction == LEFT and any(p[1] == 0 for p in rock):
        return rock

    if direction == LEFT:
        return {(p[0], p[1] - 1) for p in rock}

    if direction == RIGHT:
        return {(p[0], p[1] + 1) for p in rock}

    raise ValueError(rock, direction)


def move_downwards(rock: set[Point]) -> set[Point]:
    return {(p[0] - 1, p[1]) for p in rock}


def print_coords(coords: set[Point]) -> None:
    print()
    print()
    buf = []
    my = max(c[0] for c in coords)
    for r in range(my, -1, -1):
        for c in range(7):
            buf.append("@" if (r, c) in coords else ".")
        buf += "\n"
    print("".join(buf))


def solve(raw: str, rock_count: int) -> int:
    jets = [(-1 if j == "<" else 1) for j in raw]
    njets = len(jets)
    nblocks = len(blocks)
    tunnel = {(0, n) for n in range(7)}
    height = 0
    rock_num = 0
    jnum = 0

    add = 0
    seen = {}
    try_cache = True

    while rock_num < rock_count:
        bnum = rock_num % nblocks
        rock = blocks[bnum](height + 4)
        while True:
            check = move_sideways(rock, jets[jnum])
            jnum = (jnum + 1) % njets
            if check.isdisjoint(tunnel):
                rock = check

            check = move_downwards(rock)
            if not check.isdisjoint(tunnel):
                break
            rock = check

        tunnel.update(rock)
        height = max(p[0] for p in tunnel)
        if try_cache:
            # 1 row seems to be enough strangely..
            offsets = frozenset(((height - y), x) for y, x in tunnel if height - y <= 3)
            key = (bnum, jnum, offsets)
            if key in seen:
                try_cache = False
                # Cycle detection, find the min y-offset for each column, the wind position, and the block position
                # if we've seen the same pattern before we can add them up to < 1T, then complete the simulation
                old_count, old_height = seen[key]
                diff_height = height - old_height
                diff_count = rock_num - old_count
                skip = (rock_count - rock_num) // diff_count
                add += skip * diff_height
                rock_num += skip * diff_count
            seen[key] = (rock_num, height)
        rock_num += 1
    return height + add


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        jets = [(-1 if j == "<" else 1) for j in raw]
        njets = len(jets)
        nblocks = len(blocks)
        tunnel = {(0, n) for n in range(7)}
        height = 0
        jet_num = 0
        for rock_num in range(rock_count):
            rock = blocks[rock_num % nblocks](height + 4)
            while True:
                check = move_sideways(rock, jets[jet_num % njets])
                jet_num += 1
                if check.isdisjoint(tunnel):
                    rock = check

                check = move_downwards(rock)
                if not check.isdisjoint(tunnel):
                    break
                rock = check

            tunnel.update(rock)
            height = max(p[0] for p in tunnel)
        return height


puzzle = Puzzle(
    year=2022,
    day=17,
    test_answers=("3068", "1514285714288"),
    test_input=""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>""",
)

if __name__ == "__main__":
    puzzle.cli()
