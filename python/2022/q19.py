from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import cached_property

import aocd
import utils

parser = (
    "Blueprint {:d}: "
    "Each ore robot costs {:d} ore. "
    "Each clay robot costs {:d} ore. "
    "Each obsidian robot costs {:d} ore and {:d} clay. "
    "Each geode robot costs {:d} ore and {:d} obsidian."
)

"""
How much does a Geo robot cost?

Each ore robot costs 4 ore
Each clay robot costs 2 ore
Each obsidian robot costs 3 ore and 14 clay
Each geode robot costs 2 ore and 7 obsidian


geo = 7 * (obsidian) + 2
obsidian = 14 * (clay) + 3
clay = 2 (ore)

=> geo = 7 * (14 * (2) + 3) + 2
obsidian = 14 * (clay) + 3
clay = 2 (ore)

"""


class Kind(str, Enum):
    ORE = "ore"
    CLAY = "clay"
    OBSIDIAN = "obsidian"
    GEODE = "geode"


@dataclass(eq=True, frozen=True)
class Schematic:
    kind: Kind
    ore: int
    clay: int
    obsidian: int


@dataclass(eq=True, frozen=True)
class BluePrint:
    num: int
    ore: Schematic
    clay: Schematic
    obsidian: Schematic
    geode: Schematic

    # Since we can only produce 1 robot per tick, we must not create more robots
    # than the material we can consume in 1 tick. We don't store it on the swarm
    # since we're constantly recreating them.

    @cached_property
    def max_ore(self):
        return max(self.ore.ore, self.clay.ore, self.obsidian.ore, self.geode.ore)

    @cached_property
    def max_clay(self):
        return max(self.ore.clay, self.clay.clay, self.obsidian.clay, self.geode.clay)

    @cached_property
    def max_obsidian(self):
        return max(
            self.ore.obsidian, self.clay.obsidian, self.obsidian.obsidian, self.geode.obsidian
        )


@dataclass(eq=True, frozen=True)
class Swarm:
    blueprint: BluePrint
    step: int
    ore: int
    clay: int
    obsidian: int
    geode: int
    robot_ore: int
    robot_clay: int
    robot_obsidian: int
    robot_geode: int

    def maxed(self, kind: Kind) -> bool:
        match kind:
            case Kind.ORE:
                return (
                    self.robot_ore >= self.blueprint.max_ore
                    or self.step > 24 - 4
                    or self.ore >= self.blueprint.max_ore * (24 - self.step)
                )
            case Kind.CLAY:
                return (
                    self.robot_clay >= self.blueprint.max_clay
                    or self.step > 24 - 3
                    or self.clay >= self.blueprint.max_clay * (24 - self.step)
                )
            case Kind.OBSIDIAN:
                return (
                    self.robot_obsidian >= self.blueprint.max_obsidian
                    or self.step > 24 - 2
                    or self.obsidian >= self.blueprint.max_obsidian * (24 - self.step)
                )

            case Kind.GEODE:
                return self.step > 24 - 1

    def can_produce(self, schematic: Schematic) -> bool:
        return (
            schematic.ore <= self.ore
            and schematic.clay <= self.clay
            and schematic.obsidian <= self.obsidian
        ) and not self.maxed(schematic.kind)

    def produce(self, schematic: Schematic) -> Swarm:
        return Swarm(
            blueprint=self.blueprint,
            step=self.step + 1,
            ore=self.ore - schematic.ore + self.robot_ore,
            clay=self.clay - schematic.clay + self.robot_clay,
            obsidian=self.obsidian - schematic.obsidian + self.robot_obsidian,
            geode=self.geode + self.robot_geode,
            robot_ore=self.robot_ore + (1 if schematic.kind == Kind.ORE else 0),
            robot_clay=self.robot_clay + (1 if schematic.kind == Kind.CLAY else 0),
            robot_obsidian=self.robot_obsidian + (1 if schematic.kind == Kind.OBSIDIAN else 0),
            robot_geode=self.robot_geode + (1 if schematic.kind == Kind.GEODE else 0),
        )

    def work(self) -> list[Swarm]:
        swarms = []
        just_collect = Swarm(
            self.blueprint,
            self.step + 1,
            self.ore + self.robot_ore,
            self.clay + self.robot_clay,
            self.obsidian + self.robot_obsidian,
            self.geode + self.robot_geode,
            self.robot_ore,
            self.robot_clay,
            self.robot_obsidian,
            self.robot_geode,
        )

        bp = self.blueprint
        if self.step < 24:
            swarms.extend(
                self.produce(sch)
                for sch in [bp.ore, bp.clay, bp.obsidian, bp.geode]
                if self.can_produce(sch)
            )
        swarms.append(just_collect)
        return swarms

    def quality(self) -> int:
        return self.geode * self.blueprint.num

    def best_possible(self) -> int:
        # current number of geodes, and how many we could possibly produce if we
        # created a geobot each step
        remaining = 24 - self.step
        return self.geode + (remaining * self.robot_geode) + utils.triangle_number(remaining)


def part_one(raw: str, minutes: int) -> int:
    data = utils.Input(raw).lines().parse(parser)
    blueprints = [
        BluePrint(
            bp,
            Schematic(Kind.ORE, ore_ore, 0, 0),
            Schematic(Kind.CLAY, clay_ore, 0, 0),
            Schematic(Kind.OBSIDIAN, obs_ore, obs_clay, 0),
            Schematic(Kind.GEODE, geo_ore, 0, geo_obs),
        )
        for bp, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs in data
    ]
    qualities = []
    for bp in blueprints:
        best = Swarm(bp, 0, 0, 0, 0, 0, 1, 0, 0, 0)
        seen = set()
        queue = deque([best])
        while queue:
            swarm = queue.pop()

            if swarm.step > 24:
                continue

            if swarm in seen:
                continue
            seen.add(swarm)

            if swarm.geode > best.geode:
                best = swarm

            if swarm.best_possible() < best.geode:
                continue

            queue.extend(swarm.work())
        qualities.append(best)
    return sum(q.quality() for q in qualities)


def test():
    test_input = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""
    answer_1 = part_one(test_input)
    assert answer_1 == 33, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=19, year=2022)
    print("Part 1: ", part_one(data))
