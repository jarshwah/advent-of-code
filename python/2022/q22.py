from __future__ import annotations

import dataclasses
import enum

import aocd
from utils import Point


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
        match (turn):
            case Turn.L:
                return Facing((value.value - 1) % 4)
            case Turn.R:
                return Facing((value.value + 1) % 4)

    def move(self) -> tuple[int, int]:
        match (self):
            case Facing.R:
                return (0, 1)
            case Facing.D:
                return (1, 0)
            case Facing.L:
                return (0, -1)
            case Facing.U:
                return (-1, 0)


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
        return f"Node(row={self.row}, col={self.col}, empty={self.empty}, square={self.square})"

    def __str__(self) -> str:
        return f"Node(({self.row},{self.col}) [{self.square}]: {'.' if self.empty else '#'}"

    @property
    def square(self) -> int:
        squares = {
            (0, 1): 1,
            (0, 2): 2,
            (1, 1): 3,
            (2, 1): 4,
            (2, 0): 5,
            (3, 0): 6,
        }
        return squares[self.row // 50, self.col // 50]

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


def edge_map(row: int, col: int, facing: Facing) -> tuple[int, int, Facing]:
    """
     12
     3
     4
    65
    """
    squares = {
        (0, 1): 1,
        (0, 2): 2,
        (1, 1): 3,
        (2, 1): 4,
        (2, 0): 5,
        (3, 0): 6,
    }
    square = squares[row // 50, col // 50]
    # fmt: off
    match (square, facing):
        case (2, Facing.R): return (149 - row % 50, 99, Facing.L)
        case (2, Facing.D): return (50 + col % 50, 99, Facing.L)
        case (2, Facing.U): return (199, col - 100, Facing.U)
        case (1, Facing.L): return (149 - row % 50, 0, Facing.R)
        case (1, Facing.U): return (150 + col % 50, 0, Facing.R)
        case (3, Facing.R): return (49, 100 + row % 50, Facing.U)
        case (3, Facing.L): return (100, row % 50, Facing.D)
        case (4, Facing.R): return (49 - row % 50, 149, Facing.L)
        case (4, Facing.D): return (150 + col % 50, 49, Facing.L)
        case (5, Facing.L): return (49 - row % 50, 50, Facing.R)
        case (5, Facing.U): return (50 + col % 50, 50, Facing.R)
        case (6, Facing.R): return (149, 50 + row % 50, Facing.U)
        case (6, Facing.D): return (0, 100 + col, Facing.D)
        case (6, Facing.L): return (0, 50 + row % 50, Facing.D)
        case _: raise ValueError(square, facing)
    # fmt: on


def part_two(raw: str) -> int:
    cube_net, instr = raw.split("\n\n")
    instructions = parse_instructions(instr)
    locations = parse_locations(cube_net)
    prow, pcol = min(locations)
    facing = Facing.R
    for instruction in instructions:
        match instruction:
            case Instruction(Turn(rotation)):
                facing = facing.rotate(facing, rotation)
            case Instruction(int(steps)):
                for _ in range(steps):
                    nrow, ncol = facing.move()
                    pos = locations.get((prow + nrow, pcol + ncol))
                    if pos is None:
                        nrow, ncol, nfacing = edge_map(prow, pcol, facing)
                        if not locations[nrow, ncol].empty:
                            # Wall on edge
                            break
                        prow = nrow
                        pcol = ncol
                        facing = nfacing
                    elif pos.empty:
                        prow += nrow
                        pcol += ncol
                    else:
                        break

    return 1000 * (prow + 1) + 4 * (pcol + 1) + facing.value


def test():
    # has trailing whitespace so read from file
    test_input = open("./q22.example").read()
    answer_1 = part_one(test_input)
    assert answer_1 == 6032, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=22, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
