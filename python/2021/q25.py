import aocd


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


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=25, year=2021)
    print("Part 1: ", part_one(data))
