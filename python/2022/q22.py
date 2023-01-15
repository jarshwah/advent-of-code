from __future__ import annotations

import dataclasses
import enum
from typing import Callable

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

    def rotate(self, turn: Turn) -> Facing:
        match (turn):
            case Turn.L:
                return Facing((self.value - 1) % 4)
            case Turn.R:
                return Facing((self.value + 1) % 4)

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

    def __repr__(self) -> str:
        return f"Node(row={self.row}, col={self.col}, empty={self.empty})"

    def __str__(self) -> str:
        return f"Node(({self.row},{self.col}): {'.' if self.empty else '#'}"


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


def edge_map_2d(
    row: int, col: int, facing: Facing, locations: dict[Point, Node]
) -> tuple[int, int, Facing]:
    match facing:
        case Facing.R:
            return (row, min(nb.col for nb in locations.values() if nb.row == row), facing)
        case Facing.L:
            return (row, max(nb.col for nb in locations.values() if nb.row == row), facing)
        case Facing.D:
            return (min(nb.row for nb in locations.values() if nb.col == col), col, facing)
        case Facing.U:
            return (max(nb.row for nb in locations.values() if nb.col == col), col, facing)


def edge_map_3d(
    row: int, col: int, facing: Facing, locations: dict[Point, Node]
) -> tuple[int, int, Facing]:
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


def solve(
    raw: str, edge_map: Callable[[int, int, Facing, dict[Point, Node]], tuple[int, int, Facing]]
) -> int:
    cube_net, instr = raw.split("\n\n")
    instructions = parse_instructions(instr)
    locations = parse_locations(cube_net)
    prow, pcol = min(locations)
    facing = Facing.R
    for instruction in instructions:
        match instruction:
            case Instruction(Turn(rotation)):
                facing = facing.rotate(rotation)
            case Instruction(int(steps)):
                for _ in range(steps):
                    nrow, ncol = facing.move()
                    pos = locations.get((prow + nrow, pcol + ncol))
                    if pos is None:
                        nrow, ncol, nfacing = edge_map(prow, pcol, facing, locations)
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
    answer_1 = solve(test_input, edge_map_2d)
    assert answer_1 == 6032, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=22, year=2022)
    print("Part 1: ", solve(data, edge_map_2d))
    print("Part 2: ", solve(data, edge_map_3d))
