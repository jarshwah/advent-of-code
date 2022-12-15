import typing as t
from dataclasses import dataclass
from functools import cached_property

import aocd
import utils
from utils import Point, manhattan


@dataclass
class Sensor:
    location: Point
    beacon: Point

    @cached_property
    def manhattan(self):
        return manhattan(self.location, self.beacon)


def part_one(raw: str, row: int) -> int:
    data = (
        utils.Input(raw)
        .split("\n")
        .parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}")
    )
    sensors: list[Sensor] = []
    beacons: set[Point] = set()
    for sx, sy, bx, by in data:
        sensor = Sensor(location=(sy, sx), beacon=(by, bx))
        sensors.append(sensor)
        beacons.add(sensor.beacon)

    coverage: list[tuple[Sensor, Point]] = []
    for sensor in sensors:
        mh = sensor.manhattan
        for direction in ((-mh, 0), (0, mh), (mh, -0), (0, -mh)):
            furthest = utils.sum_points(sensor.location, direction)
            y1, y2 = sorted((sensor.location[0], furthest[0]))
            if y1 <= row <= y2:
                coverage.append((sensor, furthest))

    empty = set()
    for (sensor, furthest) in coverage:
        on_row = (row, furthest[1])
        # scan left and right while the manhattan distance works
        if manhattan(sensor.location, on_row) > sensor.manhattan:
            raise ValueError(sensor)

        empty.add(on_row)

        for direction in (utils.LEFT, utils.RIGHT):
            check = on_row
            while True:
                check = utils.sum_points(check, direction)
                mh = manhattan(sensor.location, check)
                if mh <= sensor.manhattan:
                    empty.add(check)
                    continue
                break

    return len(empty - beacons)


def part_two(raw: str, max_size: int) -> int:
    data = utils.Input(raw)
    return 1


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
    answer_2 = part_two(test_input, max_size=20)
    assert answer_1 == 26, answer_1
    assert answer_2 == 56000011, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=15, year=2022)
    print("Part 1: ", part_one(data, row=2000000))
    print("Part 2: ", part_two(data, max_size=4000000))
