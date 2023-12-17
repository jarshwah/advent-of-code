import heapq

import aocd

import utils


def get_heat(
    grid: utils.Grid,
    start: utils.Point,
    goal: utils.Point,
    start_direction: utils.Point,
    max_forward: int,
    min_forward: int,
) -> int:
    visited = {}
    queue = [(0, start, start_direction, 0)]
    while queue:
        score, current, direction, forward_steps = heapq.heappop(queue)
        if (current, direction, forward_steps) in visited:
            continue

        if current == goal and forward_steps >= min_forward:
            return score

        visited[(current, direction, forward_steps)] = score

        # Generate neighbours
        possible_directions = [direction] if forward_steps < max_forward else []
        if forward_steps >= min_forward:
            possible_directions.extend((utils.turn_left(direction), utils.turn_right(direction)))

        neighbours = [
            (node, turn)
            for turn in possible_directions
            if ((node := utils.point_add(current, turn)) in grid)
        ]
        for nb, new_direction in neighbours:
            if nb not in grid:
                continue
            heapq.heappush(
                queue,
                (
                    score + grid[nb],
                    nb,
                    new_direction,
                    forward_steps + 1 if new_direction == direction else 1,
                ),
            )

    assert False


def part_one(raw: str) -> int:
    grid = utils.Input(raw).grid_int()

    return get_heat(
        grid=grid,
        start=(0, 0),
        goal=(grid.height - 1, grid.width - 1),
        start_direction=utils.RIGHT,
        max_forward=3,
        min_forward=0,
    )


def part_two(raw: str) -> int:
    grid = utils.Input(raw).grid_int()
    return get_heat(
        grid=grid,
        start=(0, 0),
        goal=(grid.height - 1, grid.width - 1),
        start_direction=utils.RIGHT,
        max_forward=10,
        min_forward=4,
    )


def test():
    test_input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 102, answer_1
    assert answer_2 == 94, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=17, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
