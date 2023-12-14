import aocd

import utils


def tilt_west(grid: utils.Grid) -> utils.Grid:
    for rn in range(grid.height):
        last_block = -1
        for cn in range(grid.width):
            if grid[rn, cn] == "O":
                grid[rn, cn] = "."
                last_block += 1
                grid[rn, last_block] = "O"
            elif grid[rn, cn] == "#":
                last_block = cn
    return grid


def tilt_east(grid: utils.Grid) -> utils.Grid:
    for rn in range(grid.height - 1, -1, -1):
        last_block = grid.width
        for cn in range(grid.width - 1, -1, -1):
            if grid[rn, cn] == "O":
                grid[rn, cn] = "."
                last_block -= 1
                grid[rn, last_block] = "O"
            elif grid[rn, cn] == "#":
                last_block = cn
    return grid


def tilt_north(grid: utils.Grid) -> utils.Grid:
    for cn in range(grid.width):
        last_block = -1
        for rn in range(grid.height):
            if grid[rn, cn] == "O":
                grid[rn, cn] = "."
                last_block += 1
                grid[last_block, cn] = "O"
            elif grid[rn, cn] == "#":
                last_block = rn
    return grid


def tilt_south(grid: utils.Grid) -> utils.Grid:
    for cn in range(grid.width - 1, -1, -1):
        last_block = grid.height
        for rn in range(grid.height - 1, -1, -1):
            if grid[rn, cn] == "O":
                grid[rn, cn] = "."
                last_block -= 1
                grid[last_block, cn] = "O"
            elif grid[rn, cn] == "#":
                last_block = rn
    return grid


def part_one(raw: str) -> int:
    grid = utils.Input(raw).grid()
    grid = tilt_north(grid)
    return north_load(grid)


def north_load(grid: utils.Grid) -> int:
    total = 0
    for rn in range(grid.height):
        for cn in range(grid.width):
            if grid[rn, cn] == "O":
                total += grid.height - rn
    return total


def have_seen(grid: utils.Grid) -> tuple[frozenset, int]:
    load = north_load(grid)
    positions = set()
    for rn in range(grid.height):
        for cn in range(grid.width):
            if grid[rn, cn] == "O":
                positions.add((rn, cn))

    return frozenset(positions), load


def part_two(raw: str) -> int:
    grid = utils.Input(raw).grid()

    cycles = {}
    stop_cache = False
    n = 0
    target = 1e9
    while n < target:  # N = 8
        grid = tilt_north(grid)
        grid = tilt_west(grid)
        grid = tilt_south(grid)
        grid = tilt_east(grid)
        if not stop_cache:
            key = have_seen(grid)  # FOUND @ 4
            if key in cycles:
                stop_cache = True
                where = n - cycles[key]
                inc = (target - n) // where
                n += inc * where
            cycles[key] = n
        n += 1
    return north_load(grid)


def test():
    test_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 136, answer_1
    assert answer_2 == 64, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=14, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
