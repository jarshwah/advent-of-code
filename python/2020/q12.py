from __future__ import annotations

import dataclasses
import enum
import operator
import typing as t
import aocd


class Heading(enum.IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    def turn(self, lr: str, units: int) -> Heading:
        deg = units // 90
        degrees = -deg if lr == "L" else +deg
        return Heading((self + degrees) % 4)

    def move(self, units: int) -> t.List[int, int]:
        if self is Heading.E:
            return [0, units]
        elif self is Heading.W:
            return [0, -units]
        elif self is Heading.N:
            return [units, 0]
        elif self is Heading.S:
            return [-units, 0]
        raise ValueError


@dataclasses.dataclass
class Waypoint:
    ns: int = 1
    ew: int = 10

    def move(self, heading: Heading, units: int):
        if heading is Heading.N:
            self.ns += units
        elif heading is Heading.S:
            self.ns -= units
        elif heading is Heading.E:
            self.ew += units
        elif heading is Heading.W:
            self.ew -= units
        else:
            raise ValueError

    def coords(self, units: int) -> t.List[int, int]:
        return [self.ns * units, self.ew * units]

    def rotate(self, degrees: int, right=True):
        degrees = degrees // 90
        if not right:
            degrees = -degrees
        # translate left turns into equivalent right turn
        degrees = degrees % 4
        while degrees > 0:
            self.ns, self.ew = -self.ew, self.ns
            degrees -= 1


def part_one(data: str) -> int:
    start = [0, 0]
    heading = Heading.E
    for instruction in data:
        direction = instruction[0]
        units = int(instruction[1:])
        move = [0, 0]
        if direction in "LR":
            heading = heading.turn(direction, units)
        elif direction == "F":
            move = heading.move(units)
        elif direction in "NESW":
            move = Heading.__members__[direction].move(units)
        start = list(map(operator.add, start, move))
    return sum(map(abs, start))


def part_two(data: str) -> int:
    ship = [0, 0]
    waypoint = Waypoint()
    for instruction in data:
        direction = instruction[0]
        units = int(instruction[1:])
        if direction in "LR":
            waypoint.rotate(units, direction == "R")
        elif direction == "F":
            ship = list(map(operator.add, ship, waypoint.coords(units)))
        elif direction in "NESW":
            waypoint.move(Heading.__members__[direction], units)
    return sum(map(abs, ship))


if __name__ == "__main__":
    data = aocd.get_data(day=12, year=2020).splitlines()
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
