from collections import defaultdict
import utils


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


def part_two_alt(raw: str) -> int:
    """
    Scan in each direction, keeping track of the last position we've seen from
    each height. The viewing distance is the distance between the current point
    and the last known point for that height.

    Complexity is O(n). In the worst case we visit every node 4 times.

    The optimisation is to remember the previous location of each height. After
    visiting each node, we set all heights equal to and lower to the current
    position, since no smaller height can look past us.

    $ python -m timeit -n 10 -s 'import q08, aocd; data = aocd.get_data(day=8, year=2022);' 'q08.part_two_alt(data)'
        10 loops, best of 5: 19.9 msec per loop
    """
    seen = defaultdict(lambda: 1)
    grid = utils.Grid.from_number_string(raw)
    width = max(grid)[0]
    # look from the left moving right
    for row_num in range(width + 1):
        last_height = {n: 0 for n in range(10)}
        for col_num in range(width + 1):
            location = row_num, col_num
            height = grid[location]
            prev_pos = last_height[height]
            seen[location] *= col_num - prev_pos
            for n in range(height, -1, -1):
                last_height[n] = col_num

    # look from top moving down
    for col_num in range(width + 1):
        last_height = {n: 0 for n in range(10)}
        for row_num in range(width + 1):
            location = row_num, col_num
            height = grid[location]
            prev_pos = last_height[height]
            seen[location] *= row_num - prev_pos
            for n in range(height, -1, -1):
                last_height[n] = row_num

    # look from right moving left
    for row_num in range(width, -1, -1):
        last_height = {n: width for n in range(10)}
        for col_num in range(width, -1, -1):
            location = row_num, col_num
            height = grid[location]
            prev_pos = last_height[height]
            seen[location] *= prev_pos - col_num
            for n in range(height, -1, -1):
                last_height[n] = col_num

    # look from bottom moving up
    for col_num in range(width, -1, -1):
        last_height = {n: width for n in range(10)}
        for row_num in range(width, -1, -1):
            location = row_num, col_num
            height = grid[location]
            prev_pos = last_height[height]
            seen[location] *= prev_pos - row_num
            for n in range(height, -1, -1):
                last_height[n] = row_num

    return max(seen.values())


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Scan each row and column backwards and forwards counting the number of visible
        nodes and stopping when we hit a node that isn't visible.

        The 4 loops are ugly, but perform 10 times better than the naive implementation
        that visits every node and checks.

        Complexity is O(n). In the worst case we visit every node 4 times.

        $ python -m timeit -n 50 -s 'import q08, aocd; data = aocd.get_data(day=8, year=2022);' 'q08.part_one'
            50 loops, best of 5: 6.73 msec per loop
        """
        grid = utils.Grid.from_number_string
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

    def part_two(self, input: utils.Input) -> str | int:
        """
        Visit every node and check visibility along each direction.

        The implementation is easy, but the performance isn't good, as we scan over
        each node many times.

        Complexity is O(n^2). In the worst case we visit every node n/4 times.

        $ python -m timeit -n 10 -s 'import q08, aocd; data = aocd.get_data(day=8, year=2022);' 'q08.part_two'
            10 loops, best of 5: 83.6 msec per loop
        """
        grid = utils.Grid.from_number_string
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


puzzle = Puzzle(
    year=2022,
    day=8,
    test_answers=("21", "8"),
    test_input="""\
30373
25512
65332
33549
35390""",
)

if __name__ == "__main__":
    puzzle.cli()
