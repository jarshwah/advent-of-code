import aocd
import utils
import z3


def part_one(raw: str, row: int) -> int:
    data = (
        utils.Input(raw)
        .lines()
        .parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}")
    )
    empty = set()
    for sx, sy, bx, by in data:
        mh = abs(sx - bx) + abs(sy - by)
        for dy, dx in ((-mh, 0), (mh, -0)):
            cy = sy + dy
            y1, y2 = sorted((sy, cy))
            if y1 <= row <= y2:
                cx = sx + dx
                dist_rem = mh - abs(sy - row)
                empty.update(range(cx - dist_rem, cx + dist_rem + 1))
                break
    # minus the beacon on the line
    return len(empty) - 1


def part_two(raw: str, max_size: int) -> int:
    data = (
        utils.Input(raw)
        .lines()
        .parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}")
    )
    x = z3.Int("x")
    y = z3.Int("y")
    solver = z3.Solver()
    solver.add(x >= 0, x <= max_size, y >= 0, y <= max_size)
    for sx, sy, bx, by in data:
        manhattan = abs(sy - by) + abs(sx - bx)
        solver.add(z3.Abs(sy - y) + z3.Abs(sx - x) > manhattan)
    solver.check()
    model = solver.model()
    return model[x].as_long() * 4000000 + model[y].as_long()


def test():
    test_input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
    answer_1 = part_one(test_input, row=10)
    # answer_2 = part_two(test_input, max_size=20)
    assert answer_1 == 26, answer_1
    # assert answer_2 == 56000011, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=15, year=2022)
    print("Part 1: ", part_one(data, row=2000000))
    print("Part 2: ", part_two(data, max_size=4000000))
