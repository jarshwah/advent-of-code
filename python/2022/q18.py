from collections import deque

import aocd
import utils


def neighbours(cube: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    x, y, z = cube
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1


def solve(raw: str) -> tuple[int, int]:
    data = utils.Input(raw).group("\n", ",").integers
    cubes = {tuple(coords) for coords in data}
    surfaces = 6 * len(cubes)

    for cube in cubes:
        surfaces -= len([n for n in neighbours(cube) if n in cubes])

    # create empty space around the grid so we can traverse all
    # the way around and try to enter all empty spaces
    minx = min(c[0] for c in cubes) - 1
    maxx = max(c[0] for c in cubes) + 2
    miny = min(c[1] for c in cubes) - 1
    maxy = max(c[1] for c in cubes) + 2
    minz = min(c[2] for c in cubes) - 1
    maxz = max(c[2] for c in cubes) + 2

    grid = {
        (x, y, z) for x in range(minx, maxx) for y in range(miny, maxy) for z in range(minz, maxz)
    }
    missing = grid - cubes
    queue = deque([(minx, miny, minz)])
    while queue:
        check = queue.pop()
        if check in missing:
            missing.remove(check)
            queue.extend(neighbours(check))
    empty = sum(len([n for n in neighbours(cube) if n in cubes]) for cube in missing)
    return surfaces, surfaces - empty


def test():
    test_input = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
    answer_1, answer_2 = solve(test_input)
    assert answer_1 == 64, answer_1
    assert answer_2 == 58, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=18, year=2022)
    a1, a2 = solve(data)
    print("Part 1: ", a1)
    print("Part 2: ", a2)
