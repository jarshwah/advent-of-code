from __future__ import annotations
import math
from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
import utils


parser = (
    "Blueprint {:d}: "
    "Each ore robot costs {:d} ore. "
    "Each clay robot costs {:d} ore. "
    "Each obsidian robot costs {:d} ore and {:d} clay. "
    "Each geode robot costs {:d} ore and {:d} obsidian."
)


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        data = input.lines().parse(parser)
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
        qualities: list[Swarm] = []
        for bp in blueprints[:3]:
            best = Swarm(bp, 0, 0, 0, 0, 0, 1, 0, 0, 0)
            seen = set()
            queue = deque([best])
            while queue:
                swarm = queue.pop()

                if swarm.step > 32:
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
            print(best)
        return math.prod([q.geode for q in qualities])


puzzle = Puzzle(
    year=2022,
    day=192,
    test_answers=("", ""),
    test_input="""\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""",
)

if __name__ == "__main__":
    puzzle.cli()
