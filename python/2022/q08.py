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


def part_two_alt(raw: str) -> int:
    """
    Find the visibility in all directions for each node then find the best
    visibility by multiplying the visibility of each direction.

    Visibility for a direction is determined by:
        0 if the neighbour is outside the grid
        1 if the neighbour is of equal or greater height
        otherwise: the visibility of our neighbour + 1

    We can recursively check the visibility of our neighbours and cache the
    results.
    """
    grid = utils.Grid.from_number_string(raw)
    seen: dict[
        utils.Point, dict[utils.UP | utils.RIGHT | utils.DOWN | utils.LEFT, int]
    ] = defaultdict(dict)
    for point in grid:
        queue = deque([(point, direction) for direction in utils.DIRECTIONS_4])
        while queue:
            node, direction = queue.popleft()
            node_height = grid[node]
            found = seen[node].get(direction)
            if found:
                continue

            # 0 if neighbour is outside the grid
            neighbour = utils.sum_points(node, direction)
            if neighbour not in grid:
                seen[node][direction] = 0
                continue

            # 1 if neighbour is of equal or greater height
            neighbour_height = grid[neighbour]
            if neighbour_height >= node_height:
                seen[node][direction] = 1
                continue

            # otherwise, the visibility of our neighbour + 1
            if direction in seen[neighbour]:
                seen[node][direction] = seen[neighbour][direction] + 1
                continue

            # if we don't yet have neighbour visibility we add the neighbour
            # onto the queue to recursively resolve, we'll recheck later
            queue.appendleft((neighbour, direction))
            # and when that has resolved, we'll need to re-resolve ourselves
            queue.append((node, direction))

    # everything now has a visibility score, so we take the product of all directions
    # for each node and find the max
    # (52, 86) == 52 * 12 * 46 * 6 == 172224
    # TODO: some of the neighbours aren't computing properly... 🤔
    return max(math.prod(directions.values()) for directions in seen.values())


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
