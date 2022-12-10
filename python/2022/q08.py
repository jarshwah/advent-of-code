import math
from collections import defaultdict, deque

import aocd
import utils


def part_one(raw: str) -> int:
    """
    Scan each row and column backwards and forwards counting the number of visible
    nodes and stopping when we hit a node that isn't visible.

    The 4 loops are ugly, but perform 10 times better than the naive implementation
    that visits every node and checks.

    Complexity is O(n). In the worst case we visit every node 4 times.

    $ python -m timeit -n 50 -s 'import q08, aocd; data = aocd.get_data(day=8, year=2022);' 'q08.part_one(data)'
        50 loops, best of 5: 6.73 msec per loop
    """
    grid = utils.Grid.from_number_string(raw)
    can_see = set()
    width = max(grid)[0] + 1
    # look from the left
    for row_num in range(width):
        prev = -1
        for col_num in range(width):
            location = row_num, col_num
            if (height := grid[location]) > prev:
                can_see.add(location)
                prev = max(height, prev)
                continue

    # look from top
    for row_num in range(width):
        prev = -1
        for col_num in range(width):
            location = col_num, row_num
            if (height := grid[location]) > prev:
                can_see.add(location)
                prev = max(height, prev)
                continue

    # look from right
    for row_num in range(width - 1, -1, -1):
        prev = -1
        for col_num in range(width - 1, -1, -1):
            location = row_num, col_num
            if (height := grid[location]) > prev:
                can_see.add(location)
                prev = max(height, prev)
                continue

    # look from bottom
    for row_num in range(width - 1, -1, -1):
        prev = -1
        for col_num in range(width - 1, -1, -1):
            location = col_num, row_num
            if (height := grid[location]) > prev:
                can_see.add(location)
                prev = max(height, prev)
                continue

    return len(can_see)


def part_one_alt(raw: str) -> int:
    """
    Visit every node and check for visibility towards each edge.

    This is a much simpler implementation but is 10 times slower than the
    original.

    Complexity is O(n^2). In the worst case we visit every node n/4 times.

    $ python -m timeit -n 50 -s 'import q08, aocd; data = aocd.get_data(day=8, year=2022);' 'q08.part_one_alt(data)'
        50 loops, best of 5: 66.3 msec per loop
    """
    grid = utils.Grid.from_number_string(raw)
    found = 0
    for point in grid:
        height = grid[point]
        visible = False
        for direction in utils.DIRECTIONS_4:
            current = point
            if visible:
                break
            while True:
                current = utils.sum_points(current, direction)
                if current not in grid:
                    visible = True
                    break
                current_height = grid[current]
                if current_height >= height:
                    break
        if visible:
            found += 1
    return found


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
