from itertools import combinations

import aocd
import z3

import utils


def solve_xy(
    hailstone_left: tuple[utils.Point3d, utils.Point3d],
    hailstone_right: tuple[utils.Point3d, utils.Point3d],
    lower: int,
    upper: int,
) -> int:
    (x1, y1, _), (vx1, vy1, _) = hailstone_left
    (x2, y2, _), (vx2, vy2, _) = hailstone_right

    # The *paths* must intersect, they don't need to collide, so we need
    # two periods.
    p1, p2 = z3.Reals("p1 p2")
    solver = z3.Optimize()
    solver.add(p1 >= 0)
    solver.add(p2 >= 0)
    solver.add(x1 + (p1 * vx1) == x2 + (p2 * vx2))
    solver.add(y1 + (p1 * vy1) == y2 + (p2 * vy2))
    solver.add(x1 + (p1 * vx1) <= upper)
    solver.add(x1 + (p1 * vx1) >= lower)
    solver.add(y1 + (p1 * vy1) <= upper)
    solver.add(y1 + (p1 * vy1) >= lower)

    if solver.check() == z3.sat:
        return True
    return False


def solve_xyz(
    h1: tuple[utils.Point3d, utils.Point3d],
    h2: tuple[utils.Point3d, utils.Point3d],
    h3: tuple[utils.Point3d, utils.Point3d],
) -> int:
    vector = z3.Reals("x y z")
    velocity = z3.Reals("xv yv zv")
    periods = z3.Reals("p1 p2 p3")
    solver = z3.Solver()
    for h, p in zip((h1, h2, h3), periods):
        for i in range(3):
            solver.add(h[0][i] + (p * h[1][i]) == vector[i] + (p * velocity[i]))
    assert solver.check() == z3.sat
    model = solver.model()
    return sum(model[v].as_long() for v in vector)


def part_one(raw: str, lower: int, upper: int) -> int:
    hailstones = []
    for line in utils.Input(raw).lines().strings:
        pos, vel = line.split(" @ ")
        x, y, z = [int(p) for p in pos.split(", ")]
        vx, vy, vz = [int(v) for v in vel.split(", ")]
        hailstones.append(((x, y, z), (vx, vy, vz)))
    return sum(solve_xy(h1, h2, lower, upper) for h1, h2 in combinations(hailstones, 2))


def part_two(raw: str) -> int:
    hailstones = []
    for line in utils.Input(raw).lines().strings[:3]:
        pos, vel = line.split(" @ ")
        x, y, z = [int(p) for p in pos.split(", ")]
        vx, vy, vz = [int(v) for v in vel.split(", ")]
        hailstones.append(((x, y, z), (vx, vy, vz)))
    return solve_xyz(*hailstones)


def test():
    test_input = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    answer_1 = part_one(test_input, 7, 27)
    answer_2 = part_two(test_input)
    assert answer_1 == 2, answer_1
    assert answer_2 == 47, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=24, year=2023)
    print("Part 1: ", part_one(data, 200000000000000, 400000000000000))
    print("Part 2: ", part_two(data))
