import aocd
from parse import parse

import utils


def resolve(data: str) -> tuple[int, int, int, int]:
    x1, x2, y1, y2 = parse("target area: x={:d}..{:d}, y={:d}..{:d}", data)
    return x1, x2, y1, y2


def part_one(data: str) -> int:
    x1, x2, y1, y2 = resolve(data)
    return utils.triangle_number(abs(y1 + 1))


def part_two(data: str) -> int:
    x1, x2, y1, y2 = resolve(data)
    # Can't throw it higher than the highest, otherwise step 2 falls below the box
    yv_max = abs(y1 + 1)
    # Can't throw it lower than the bottom, otherwise it sinks past the box
    yv_min = y1
    # Can't throw it past the box, it won't come back
    xv_max = x2
    # Have to throw it hard enough so that drag will 0 out at the start of the box
    # This is the minimum triange number >= x1
    xv_min = next(check for check in range(1, x1) if utils.triangle_number(check) >= x1)

    # targeting go brrrrrrrrrrrrrrrrrrrr
    found = 0
    checked = 0
    for xs in range(xv_min, xv_max + 1):
        for ys in range(yv_min, yv_max + 1):
            x, y = 0, 0
            xv, yv = xs, ys
            while not ((x > x2) or (x < x1 and xv == 0) or y < y1):
                checked += 1
                x += xv
                y += yv
                if x1 <= x <= x2 and y1 <= y <= y2:
                    found += 1
                    break
                xv = max(0, xv - 1)
                yv -= 1
    print(f"{checked=} {xv_min=} {xv_max=} {yv_min=} {yv_max=}")
    return found


def test():
    test_input = "target area: x=20..30, y=-10..-5"
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 45, answer_1
    assert answer_2 == 112, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=17, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
