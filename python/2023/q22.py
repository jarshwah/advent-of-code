from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cached_property
from graphlib import TopologicalSorter

import aocd

import utils

"""
x1 - x2 = width
y1 - y2 = depth
z1 - z2 = height

z=0: on the ground
"""


@dataclass
class Brick:
    number: int
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int
    stacked_beneath: set[Brick] = field(default_factory=set)
    stacked_on: set[Brick] = field(default_factory=set)

    @cached_property
    def coordinates_xy(self) -> set[tuple[int, int]]:
        return {(x, y) for x in range(self.x1, self.x2 + 1) for y in range(self.y1, self.y2 + 1)}

    def drop_it(self, down_to: int) -> None:
        height = self.z2 - self.z1
        self.z1 = down_to
        self.z2 = down_to + height

    def __str__(self) -> str:
        return f"({self.x1}->{self.x2}, {self.y1}->{self.y2}, {self.z1}->{self.z2})"

    def __hash__(self) -> int:
        return hash(self.number)

    def __repr__(self) -> str:
        return f"Brick {self.number}: ({self.x1},{self.x2}), ({self.y1}, {self.y2}), ({self.z1}, {self.z2})"


def print_dependencies(brick: Brick) -> None:
    print(
        f"{[b.number for b in brick.stacked_on]} <- {brick.number} -> {[b.number for b in brick.stacked_beneath]}"
    )


def both_parts(raw: str) -> tuple[int, int]:
    data = utils.Input(raw).lines().strings
    bricks: list[Brick] = []
    min_x, max_x = 1e9, -1
    min_y, max_y = 1e9, -1
    for number, line in enumerate(data):
        x1, y1, z1, x2, y2, z2 = [int(x) for side in line.split("~") for x in side.split(",")]
        bricks.append(Brick(number, *sorted([x1, x2]), *sorted([y1, y2]), *sorted([z1, z2])))
        min_x, max_x = min(min_x, x1), max(max_x, x2)
        min_y, max_y = min(min_y, y1), max(max_y, y2)

    # Track the height of each coordinate and the brick at that height
    height_map: dict[tuple[int, int], tuple[int, Brick | None]] = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            height_map[(x, y)] = (-1, None)

    # drop from lowest to highest
    bricks.sort(key=lambda b: b.z1)
    for brick in bricks:
        # Find the highest point on the ground below, and any bricks we meet at that height
        possible_z = 0
        stacked_beneath = defaultdict(set[Brick])
        for x, y in brick.coordinates_xy:
            top, top_brick = height_map[(x, y)]
            possible_z = max(possible_z, top + 1)
            if top_brick:
                stacked_beneath[top + 1].add(top_brick)

        brick.drop_it(possible_z)

        # If we fall on a brick, connect them together
        for stacked_brick in stacked_beneath[possible_z]:
            stacked_brick.stacked_beneath.add(brick)
            brick.stacked_on.add(stacked_brick)

        # Then update the height map
        for x, y in brick.coordinates_xy:
            height_map[(x, y)] = (brick.z2, brick)

    # Now check every brick, if the bricks stacked directly on top only have a single brick beneath them,
    # we're unstable.
    stable_bricks = []
    unstable_bricks = []
    for brick in bricks:
        dependents = {len(on_top.stacked_on) for on_top in brick.stacked_beneath}
        if 1 in dependents:
            unstable_bricks.append(brick)
            continue
        stable_bricks.append(brick)
    num_stable = len(stable_bricks)

    # Now recursively check for chain reactions
    chain_reactions = sum(tumble_topo(brick) for brick in unstable_bricks)
    return num_stable, chain_reactions


def tumble_topo(brick: Brick) -> int:
    # We need to tumble the bricks in topological order, not dfs order, otherwise
    # dependents will still be standing.
    # eg:
    #
    #    _______
    #    | | |   <-- but when we get here in dfs, only the left most collapses and the above stands
    #   ______   <-- and even this
    #    |  |    <-- we can delete both of these
    #   -------  <-- delete
    #
    graph = TopologicalSorter()
    queue = deque(brick.stacked_beneath)
    while queue:
        curr = queue.popleft()
        graph.add(curr, *curr.stacked_on)
        queue.extend(curr.stacked_beneath)

    tumbled = {brick}
    for brick in graph.static_order():
        if len(brick.stacked_on - tumbled) == 0:
            tumbled.add(brick)
    # The removed node is not tumbled, so subtract 1
    return len(tumbled) - 1


def test():
    test_input = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
    answer_1, answer_2 = both_parts(test_input)
    assert answer_1 == 5, answer_1
    assert answer_2 == 7, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=22, year=2023)
    a1, a2 = both_parts(data)
    print("Part 1: ", a1)
    print("Part 2: ", a2)
