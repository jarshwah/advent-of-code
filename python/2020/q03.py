import typing as t

import aocd


def traverse(treemap: t.List[str], down: int, right: int) -> int:
    width = len(treemap[0])
    depth = len(treemap)
    pos = (0, 0)
    ouchies = 0
    while pos < (depth, 0):
        if treemap[pos[0]][pos[1]] == "#":
            ouchies += 1
        pos = pos[0] + down, (pos[1] + right) % width
    return ouchies


def part_one(treemap: t.List[str]) -> int:
    return traverse(treemap, 1, 3)


def part_two(treemap: t.List[str]) -> int:
    return (
        traverse(treemap, 1, 1)
        * traverse(treemap, 1, 3)
        * traverse(treemap, 1, 5)
        * traverse(treemap, 1, 7)
        * traverse(treemap, 2, 1)
    )


if __name__ == "__main__":
    treemap = aocd.get_data(day=3, year=2020).splitlines()
    print("Part 1: ", part_one(treemap))
    print("Part 2: ", part_two(treemap))
