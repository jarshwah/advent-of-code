from __future__ import annotations

import dataclasses
import enum

import aocd
from utils import Input, Point


class Turn(str, enum.Enum):
    L = "L"
    R = "R"


class Facing(enum.IntEnum):
    R = 0
    D = 1
    L = 2
    U = 3

    @classmethod
    def rotate(cls, value: Facing, turn: Turn) -> Facing:
        # fmt: off
        match (value, turn):
            case (Facing.L, Turn.L): return Facing.D
            case (Facing.L, Turn.R): return Facing.U

            case (Facing.U, Turn.L): return Facing.L
            case (Facing.U, Turn.R): return Facing.R

            case (Facing.R, Turn.L): return Facing.U
            case (Facing.R, Turn.R): return Facing.D

            case (Facing.D, Turn.L): return Facing.R
            case (Facing.D, Turn.R): return Facing.L
        # fmt: on


@dataclasses.dataclass
class Instruction:
    move: int | Turn


@dataclasses.dataclass
class Node:
    row: int
    col: int
    empty: bool
    left: Node | None = None
    up: Node | None = None
    right: Node | None = None
    down: Node | None = None

    def __repr__(self) -> str:
        return f"Node(row={self.row}, col={self.col}, empty={self.empty})"

    def __str__(self) -> str:
        return f"Node(({self.row},{self.col}): {'.' if self.empty else '#'})"

    def resolve_neighbours_plane(self, locations: dict[Point, Node]):
        right = (self.row, self.col + 1)
        if right not in locations:
            right = (self.row, min(nb.col for nb in locations.values() if nb.row == self.row))
        self.right = locations[right]

        left = (self.row, self.col - 1)
        if left not in locations:
            left = (self.row, max(nb.col for nb in locations.values() if nb.row == self.row))
        self.left = locations[left]

        down = (self.row + 1, self.col)
        if down not in locations:
            down = (min(nb.row for nb in locations.values() if nb.col == self.col), self.col)
        self.down = locations[down]

        up = (self.row - 1, self.col)
        if up not in locations:
            up = (max(nb.row for nb in locations.values() if nb.col == self.col), self.col)
        self.up = locations[up]


@dataclasses.dataclass
class Map:
    pointer: Node
    direction: Facing
    locations: dict[Point, Node]
    instructions: int

    def move(self, steps: int) -> Node:
        # fmt: off
        match (self.direction):
            case Facing.L: attr = "left"
            case Facing.U: attr = "up"
            case Facing.R: attr = "right"
            case Facing.D: attr = "down"
            case _: raise ValueError(self.direction)
        # fmt: on
        curr = self.pointer
        for _ in range(steps):
            check: Node = getattr(curr, attr)
            if check.empty:
                curr = check
                continue
            break
        self.pointer = curr

    def process_instruction(self, instruction: Instruction):
        match (instruction):
            case Instruction(int(steps)):
                self.move(steps)
            case Instruction(Turn(rotation)):
                self.direction = Facing.rotate(self.direction, rotation)
            case _:
                raise ValueError(instruction)
        # self.draw()

    def simulate(self) -> int:
        self.assert_nodes_have_neighbours()
        for instruction in self.instructions:
            self.process_instruction(instruction)
        row = self.pointer.row
        col = self.pointer.col
        return (1000 * (row + 1)) + (4 * (col + 1)) + self.direction.value

    def assert_nodes_have_neighbours(self):
        for node in self.locations.values():
            assert node.right, node
            assert node.down, node
            assert node.left, node
            assert node.up, node

    def draw(self):
        print(end="\n\n")
        facing = ">"
        # fmt: off
        if self.direction == Facing.L: facing = "<"
        elif self.direction == Facing.R: facing = ">"
        elif self.direction == Facing.D: facing = "v"
        elif self.direction == Facing.U: facing = "^"
        # fmt: on
        maxr = max(point[0] for point in self.locations)
        maxc = max(point[1] for point in self.locations)
        for rn in range(maxr + 1):
            line = ""
            for cn in range(maxc + 1):
                if self.pointer.row == rn and self.pointer.col == cn:
                    line += facing
                    continue
                loc = self.locations.get((rn, cn))
                if not loc:
                    line += " "
                    continue
                line += "." if loc.empty else "#"
            print(line)


def parse_instructions(instructions: str) -> list[Instruction]:
    tokens = instructions.replace("L", " L ").replace("R", " R ").split(" ")
    return [Instruction(int(t) if t.isdigit() else Turn(t)) for t in tokens]


def parse_locations(grid: str) -> dict[Point, Node]:
    locations = {}
    lines = grid.splitlines()
    maxc = max(len(r) for r in lines)
    for rn in range(len(lines)):
        for cn in range(maxc):
            try:
                char = lines[rn][cn]
            except IndexError:
                # There's no trailing whitespace..
                continue
            if char == " ":
                continue
            empty = True if char == "." else False
            locations[rn, cn] = Node(row=rn, col=cn, empty=empty)
    return locations


def part_one(raw: str) -> int:
    grid, instr = raw.split("\n\n")
    instructions = parse_instructions(instr)
    locations = parse_locations(grid)
    for node in locations.values():
        node.resolve_neighbours_plane(locations)
    pointer = locations[min(locations)]
    state = Map(pointer=pointer, direction=Facing.R, locations=locations, instructions=instructions)
    return state.simulate()


def part_two(raw: str) -> int:
    data = Input(raw)
    return 1


def test():
    # has trailing whitespace so read from file
    example = """        ...#
        .#..
        #...
        ....
...#.D.....#
........#...
B.#....#...A
.....C....#.
        ...#....
        .....#..
        .#......
        ......#.
"""
    test_input = open("./q22.example").read()
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 6032, answer_1
    assert answer_2 == 1, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=22, year=2022)
    print("Part 1: ", part_one(data))
    # print("Part 2: ", part_two(data))
