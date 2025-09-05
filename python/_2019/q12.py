import itertools
import math
import operator
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce

import utils


def cmp(ln: int, rn: int) -> int:
    if ln < rn:
        return 1
    if ln > rn:
        return -1
    return 0


@dataclass
class Moon:
    x: int
    y: int
    z: int
    vx: int = 0
    vy: int = 0
    vz: int = 0

    def apply_velocity(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def energy(self) -> int:
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (
            abs(self.vx) + abs(self.vy) + abs(self.vz)
        )

    def __lshift__(self, that: "Moon") -> "Moon":
        self.vx += cmp(self.x, that.x)
        self.vy += cmp(self.y, that.y)
        self.vz += cmp(self.z, that.z)
        return that


def simulate(moons: list[Moon]) -> None:
    for lm, rm in itertools.combinations(moons, 2):
        lm << rm << lm
    for moon in moons:
        moon.apply_velocity()


class Puzzle(utils.Puzzle):
    """--- Day 12: The N-Body Problem ---"""

    def part_one(self, input: utils.Input) -> str | int:
        moons = [
            Moon(x=ps["x"], y=ps["y"], z=ps["z"])
            for ps in input.lines().parse("<x={x:d}, y={y:d}, z={z:d}>")
        ]
        for _ in range(100 if self.testing else 1000):
            simulate(moons)
        return sum(m.energy() for m in moons)

    def part_two(self, input: utils.Input) -> str | int:
        og_moons = [
            Moon(x=ps["x"], y=ps["y"], z=ps["z"])
            for ps in input.lines().parse("<x={x:d}, y={y:d}, z={z:d}>")
        ]
        cycles: list[int] = []
        # Each axis is independent. Simulate until it cycles. Then take the
        # LCM of all 3 axis cycles to find the time-step where the moons repeat
        # an energy state.
        for axis in ["x", "y", "z"]:
            seen = {}
            pg = operator.attrgetter(axis)
            vg = operator.attrgetter(f"v{axis}")
            moons = deepcopy(og_moons)
            for n in itertools.count(0):
                key = tuple([(pg(mn), vg(mn)) for mn in moons])
                if key in seen:
                    cycles.append(n)
                    break
                seen[key] = n
                simulate(moons)
        return reduce(math.lcm, cycles)


puzzle = Puzzle(
    year=2019,
    day=12,
    test_answers=("1940", "4686774924"),
    test_input="""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""",
)

if __name__ == "__main__":
    puzzle.cli()
