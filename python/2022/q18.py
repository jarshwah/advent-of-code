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
    cubes = {(x, y, z) for x, y, z in data}
    surfaces = 6 * len(cubes)
    empty = 0
    for cube in cubes:
        surfaces -= len([n for n in neighbours(cube) if n in cubes])

    # create empty space around the grid so we can traverse all
    # the way around and try to enter all empty spaces
    minx = min(x for x, y, z in cubes) - 1
    maxx = max(x for x, y, z in cubes) + 2
    miny = min(y for x, y, z in cubes) - 1
    maxy = max(y for x, y, z in cubes) + 2
    minz = min(z for x, y, z in cubes) - 1
    maxz = max(z for x, y, z in cubes) + 2

    grid = {
        (x, y, z) for x in range(minx, maxx) for y in range(miny, maxy) for z in range(minz, maxz)
    }
    missing = grid - cubes
    queue = deque([(minx, miny, minz)])
    while queue:
        check = queue.pop()
        if check in missing:
            missing.remove(check)
            queue.extend(nb for nb in neighbours(check) if nb in grid)
    for cube in missing:
        empty -= len([n for n in neighbours(cube) if n in cubes])
    return surfaces, surfaces + empty


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
