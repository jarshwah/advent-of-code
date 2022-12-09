import aocd
import utils


def part_one(raw: str) -> int:
    grid = utils.Grid.from_number_string(raw)
    can_see = set()
    width = max(grid)[0] + 1
    # look from the left
    for row_num in range(width):
        prev = -1
        for col_num in range(width):
            location = row_num, col_num
            if grid[location] > prev:
                can_see.add(location)
                prev = max(grid[location], prev)
                continue

    # look from top
    for row_num in range(width):
        prev = -1
        for col_num in range(width):
            location = col_num, row_num
            if grid[location] > prev:
                can_see.add(location)
                prev = max(grid[location], prev)
                continue

    # look from right
    for row_num in range(width - 1, -1, -1):
        prev = -1
        for col_num in range(width - 1, -1, -1):
            location = row_num, col_num
            if grid[location] > prev:
                can_see.add(location)
                prev = max(grid[location], prev)
                continue

    # look from bottom
    for row_num in range(width - 1, -1, -1):
        prev = -1
        for col_num in range(width - 1, -1, -1):
            location = col_num, row_num
            if grid[location] > prev:
                can_see.add(location)
                prev = max(grid[location], prev)
                continue

    return len(can_see)


def part_two(raw: str) -> int:
    grid = utils.Grid.from_number_string(raw)
    best_view = 0
    for point in grid:
        view = 1
        height = grid[point]
        for direction in utils.DIRECTIONS_4:
            current = point
            count = 0
            while True:
                current = utils.sum_points(current, direction)
                if current not in grid:
                    break
                count += 1
                if grid[current] >= height:
                    break
            view *= count
        best_view = max(best_view, view)
    return best_view


def test():
    test_input = """30373
25512
65332
33549
35390"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 21, answer_1
    assert answer_2 == 8, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=8, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
