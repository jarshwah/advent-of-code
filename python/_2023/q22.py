from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cached_property
from graphlib import TopologicalSorter

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


def tumble_topo(brick: Brick) -> int:
    # Construct graph with inverted directions
    graph = TopologicalSorter[Brick]()
    seen = set()
    queue = deque([brick])
    while queue:
        curr = queue.popleft()
        if curr in seen:
            continue
        seen.add(curr)
        graph.add(curr, *curr.stacked_on)
        queue.extend(curr.stacked_beneath)

    tumbled = {brick}
    for brick in graph.static_order():
        if len(brick.stacked_on - tumbled) == 0:
            tumbled.add(brick)
    # The removed node is not tumbled, so subtract 1
    return len(tumbled) - 1


class Puzzle(utils.Puzzle):
    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        data = input.lines().strings
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
            max_height = -1
            bricks_below = set()
            for coord in brick.coordinates_xy:
                height, brck = height_map[coord]
                if height > max_height:
                    max_height = height
                    bricks_below = {brck} if brck else set()
                elif height == max_height and brck:
                    bricks_below.add(brck)

            # drop the brick to the ground
            brick.drop_it(max_height + 1)

            # Update dependency graph
            for brck in bricks_below:
                brick.stacked_on.add(brck)
                brck.stacked_beneath.add(brick)

            # Update the height map
            for coord in brick.coordinates_xy:
                height_map[coord] = (brick.z2, brick)

        # Find all bricks that have at least 1 brick stacked on them that have no other support
        stable_bricks = []
        unstable_bricks = []
        for brick in bricks:
            for stacked_brick in brick.stacked_beneath:
                if len(stacked_brick.stacked_on) == 1:
                    unstable_bricks.append(brick)
                    break
            else:
                stable_bricks.append(brick)
        num_stable = len(stable_bricks)

        # Now recursively check for chain reactions
        chain_reactions = sum(tumble_topo(brick) for brick in unstable_bricks)
        return num_stable, chain_reactions


puzzle = Puzzle(
    year=2023,
    day=22,
    test_answers=("5", "7"),
    test_input="""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""",
    both=True,
)

if __name__ == "__main__":
    puzzle.cli()
