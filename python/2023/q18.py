import aocd

import utils

DIRS = {
    "R": utils.RIGHT,
    "L": utils.LEFT,
    "U": utils.UP,
    "D": utils.DOWN,
    "0": utils.RIGHT,
    "2": utils.LEFT,
    "3": utils.UP,
    "1": utils.DOWN,
}


def part_one(raw: str) -> int:
    current = (0, 0)
    points = [current]
    lines = utils.Input(raw).lines().strings
    for line in lines:
        direction, steps_s, color = line.split()
        for _ in range(int(steps_s)):
            current = utils.point_add(current, DIRS[direction])
            points.append(current)
    return utils.area_including_boundary(points)


def part_two(raw: str) -> int:
    lines = utils.Input(raw).lines().strings
    first = (0, 0)
    current = first
    num_points = 0
    area_gen = utils.shoelace_iter(first)
    next(area_gen)
    for line in lines:
        _, _, color = line.split()
        steps = int(color[2:7], 16)
        direction = color[7]
        num_points += steps
        current = utils.point_add(current, DIRS[direction], steps)
        area_gen.send(current)
    area = next(area_gen)
    return utils.picks_theorem(num_points, area)


def test():
    test_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 62, answer_1
    assert answer_2 == 952408144115, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=18, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
