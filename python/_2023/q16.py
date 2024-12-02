from collections import deque

import aocd

import utils


def num_energized(grid: utils.Grid, start: utils.Point, direction: utils.Point) -> int:
    energized = set()
    seen = set()
    queue = deque([(start, direction)])
    while queue:
        current, direction = queue.pop()
        if current not in grid:
            continue
        if (current, direction) in seen:
            continue
        seen.add((current, direction))
        energized.add(current)
        match (grid[current], direction):
            case (".", _):
                energized.add(current)
                queue.appendleft((utils.point_add(current, direction), direction))

            case ("-", (0, _)):  # left/right
                queue.appendleft((utils.point_add(current, direction), direction))
            case ("-", _):
                queue.appendleft((utils.point_add(current, utils.LEFT), utils.LEFT))
                queue.appendleft((utils.point_add(current, utils.RIGHT), utils.RIGHT))

            case ("|", (_, 0)):  # up/down
                queue.appendleft((utils.point_add(current, direction), direction))
            case ("|", _):
                queue.appendleft((utils.point_add(current, utils.UP), utils.UP))
                queue.appendleft((utils.point_add(current, utils.DOWN), utils.DOWN))

            case ("/", _):
                # Rotate
                dr, dc = direction
                new_dir = (-dc, -dr)
                queue.appendleft((utils.point_add(current, new_dir), new_dir))

            case ("\\", _):
                # Rotate
                dr, dc = direction
                new_dir = (dc, dr)
                queue.appendleft((utils.point_add(current, new_dir), new_dir))

            case _:
                raise ValueError(current, direction)
    return len(energized)


def part_one(raw: str) -> int:
    grid = utils.Input(raw).grid()
    return num_energized(grid, (0, 0), utils.RIGHT)


def part_two(raw: str) -> int:
    grid = utils.Input(raw).grid()
    starting_positions = []
    for p in grid:
        if p[0] == 0:
            starting_positions.append((p, utils.DOWN))
        if p[1] == 0:
            starting_positions.append((p, utils.RIGHT))
        if p[0] == grid.height - 1:
            starting_positions.append((p, utils.UP))
        if p[1] == grid.width - 1:
            starting_positions.append((p, utils.LEFT))
    return max(num_energized(grid, start, direction) for start, direction in starting_positions)


def test():
    test_input = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 46, answer_1
    assert answer_2 == 51, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=16, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
