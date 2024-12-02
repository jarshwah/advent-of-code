import aocd


def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()


def part_one(data: str) -> int:
    grid = [[ch for ch in line] for line in data.splitlines()]
    row_size = len(grid)
    col_size = len(grid[0])
    for step in range(1, 10000):
        moved = False
        new_grid = [[ch for ch in line] for line in grid]
        for ri in range(row_size):
            for ci in range(col_size):
                next_ci = (ci + 1) % col_size
                if grid[ri][ci] == ">" and grid[ri][next_ci] == ".":
                    moved = True
                    new_grid[ri][ci] = "."
                    new_grid[ri][next_ci] = ">"
        grid = new_grid
        new_grid = [[ch for ch in line] for line in grid]
        for ri in range(row_size):
            for ci in range(col_size):
                next_ri = (ri + 1) % row_size
                if grid[ri][ci] == "v" and grid[next_ri][ci] == ".":
                    moved = True
                    new_grid[ri][ci] = "."
                    new_grid[next_ri][ci] = "v"
        if not moved:
            return step
        grid = new_grid
    return -1


def single_pass(data: str) -> int:
    """
    Start at the bottom and work up to avoid having to do a RIGHT pass then a
    DOWN pass. We can check the previous square and move it RIGHT if it exists,
    otherwise check the square above and move it DOWN.

    This is actually slower (just).. ended up being more complicated than I
    initially thought it could be.
    """
    grid = [list(line) for line in data.splitlines()]
    row_size = len(grid)
    col_size = len(grid[0])
    for step in range(1, 10000):
        moved = False
        new_grid = [list(line) for line in grid]
        for ri in range(row_size - 1, -1, -1):
            prev_ri = ri - 1

            for ci in range(col_size - 1, -1, -1):
                prev_ci = ci - 1
                next_ci = (ci + 1) % col_size
                if grid[ri][ci] == "v":
                    # We can never move into a spot currently occupied by a southerner
                    continue

                if grid[ri][ci] == ".":
                    if grid[ri][prev_ci] == ">":
                        # Move into the free spot
                        moved = True
                        new_grid[ri][ci] = ">"
                        # Don't overwrite a processed square
                        if prev_ci != -1 or new_grid[ri][prev_ci] != "v":
                            new_grid[ri][prev_ci] = "."
                    elif grid[prev_ri][ci] == "v":
                        moved = True
                        new_grid[ri][ci] = "v"
                        new_grid[prev_ri][ci] = "."

                if grid[ri][ci] == ">" and grid[prev_ri][ci] == "v" and grid[ri][next_ci] == ".":
                    # If righty will move out of the way, we can move down into it later
                    moved = True
                    new_grid[ri][ci] = "v"
                    new_grid[prev_ri][ci] = "."

        if not moved:
            return step
        grid = new_grid
    return step


def test():
    test_input = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
    answer_1 = part_one(test_input)
    assert answer_1 == 58, answer_1
    answer_1 = single_pass(test_input)
    assert answer_1 == 58, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=25, year=2021)
    print("Part 1: ", part_one(data))
