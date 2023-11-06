from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from functools import cache
from typing import Iterable, Optional

import aocd


class Amphipod(IntEnum):
    A = 1
    B = 10
    C = 100
    D = 1000


@dataclass(frozen=True)
class Maze:
    hallway: tuple[int, ...]
    A: tuple[int, ...]
    B: tuple[int, ...]
    C: tuple[int, ...]
    D: tuple[int, ...]
    room_size: int

    @classmethod
    def from_allocations(cls, allocations: dict[str, list[str]]) -> Maze:
        hallway = tuple([0] * 11)
        A = tuple([Amphipod[x].value for x in allocations["A"]])
        B = tuple([Amphipod[x].value for x in allocations["B"]])
        C = tuple([Amphipod[x].value for x in allocations["C"]])
        D = tuple([Amphipod[x].value for x in allocations["D"]])
        return Maze(hallway=hallway, A=A, B=B, C=C, D=D, room_size=len(A))

    def is_solved(self) -> bool:
        return (
            sum(self.hallway) == 0
            and sum(self.A) == Amphipod.A * self.room_size
            and sum(self.B) == Amphipod.B * self.room_size
            and sum(self.C) == Amphipod.C * self.room_size
            and sum(self.D) == Amphipod.D * self.room_size
        )

    def hallway_clear(self, from_pos: int, to_pos: int) -> bool:
        if from_pos < to_pos:
            return sum(self.hallway[from_pos + 1 : to_pos + 1]) == 0
        return sum(self.hallway[to_pos:from_pos]) == 0

    def move_to_home(self, amph: Amphipod, from_hallway: int) -> tuple[Optional[Maze], int]:
        entrance = self.room_entrance(amph)
        if not self.hallway_clear(from_hallway, entrance):
            return None, 0
        room = self.room_for(amph)
        if any((check not in (0, amph)) for check in room):
            # Can't move into a room if a different type still in there
            return None, 0
        free_position, _ = max((idx, check) for idx, check in enumerate(room) if check == 0)
        energy = (abs(from_hallway - entrance) * amph.value) + ((free_position + 1) * amph.value)
        new_hallway = list(self.hallway)
        new_hallway[from_hallway] = 0
        new_room = list(room)
        new_room[free_position] = amph.value
        new_maze = Maze(
            tuple(new_hallway),
            tuple(new_room) if amph == Amphipod.A else self.A,
            tuple(new_room) if amph == Amphipod.B else self.B,
            tuple(new_room) if amph == Amphipod.C else self.C,
            tuple(new_room) if amph == Amphipod.D else self.D,
            self.room_size,
        )
        return new_maze, energy

    def move_to_hallway(
        self, room: tuple[int, ...], room_type: Amphipod
    ) -> Iterable[tuple[Maze, int]]:
        if all((amph in (room_type.value, 0)) for amph in room):
            # all in their rightful home, no need to move
            return
        position, amph = next((position, amph) for position, amph in enumerate(room) if amph != 0)
        room_entrance = self.room_entrance(room_type)
        for hall_position in (0, 1, 3, 5, 7, 9, 10):
            if self.hallway_clear(room_entrance, hall_position):
                energy = ((position + 1) * amph) + (abs(room_entrance - hall_position) * amph)
                new_hallway = list(self.hallway)
                new_hallway[hall_position] = amph
                new_room = list(room)
                new_room[position] = 0
                new_maze = Maze(
                    tuple(new_hallway),
                    tuple(new_room) if room_type == Amphipod.A else self.A,
                    tuple(new_room) if room_type == Amphipod.B else self.B,
                    tuple(new_room) if room_type == Amphipod.C else self.C,
                    tuple(new_room) if room_type == Amphipod.D else self.D,
                    self.room_size,
                )
                yield new_maze, energy

    def room_for(self, amph: Amphipod) -> tuple[int, ...]:
        # fmt: off
        match amph:
            case Amphipod.A: return self.A
            case Amphipod.B: return self.B
            case Amphipod.C: return self.C
            case Amphipod.D: return self.D
        # fmt: on

    def room_entrance(self, amph: Amphipod) -> int:
        # fmt: off
        match amph:
            case Amphipod.A: return 2
            case Amphipod.B: return 4
            case Amphipod.C: return 6
            case Amphipod.D: return 8
        # fmt: on

    def moves(self) -> Iterable[tuple[Maze, int]]:
        for pos, amph in enumerate(self.hallway):
            if amph == 0:
                continue
            amphipod = Amphipod(amph)
            new_maze, cost = self.move_to_home(amphipod, pos)
            if new_maze:
                yield (new_maze, cost)

        for room, room_type in [
            (self.A, Amphipod.A),
            (self.B, Amphipod.B),
            (self.C, Amphipod.C),
            (self.D, Amphipod.D),
        ]:
            yield from self.move_to_hallway(room, room_type)

    def print(self):
        """
        #############
        #..2......9.#
        ###B#C#B#D###
          #A#D#C#A#
          #########
        """
        print("#############")
        print("#", end="")
        for hw in self.hallway:
            print(self._c(hw), end="")
        print("#")
        for n in range(self.room_size):
            wrap = "##" if n == 0 or n == self.room_size - 1 else "  "
            print(
                f"{wrap}#{self._c(self.A[n])}#{self._c(self.B[n])}#{self._c(self.C[n])}#{self._c(self.D[n])}#{wrap}"
            )
        print("  #########  ")

    def _c(self, num) -> str:
        # fmt: off
        match num:
            case 0: return "."
            case 1: return "A"
            case 10: return "B"
            case 100: return "C"
            case 1000: return "D"
        # fmt: on


@cache
def solve(maze: Maze, energy: int) -> int:
    if maze.is_solved():
        return energy

    min_energy = 1e9
    for new_maze, move_energy in maze.moves():
        new_energy = solve(new_maze, energy + move_energy)
        if new_energy is None:
            continue
        min_energy = min(min_energy, new_energy)
    return min_energy


def parse_maze(data: str, unfolded: bool = False):
    maze = defaultdict(list)
    for line in data.splitlines():
        if result := re.search(r"#(\w)#(\w)#(\w)#(\w)", line):
            a, b, c, d = result.groups()
            maze["A"].append(a)
            maze["B"].append(b)
            maze["C"].append(c)
            maze["D"].append(d)
        if unfolded and len(maze["A"]) == 1:
            maze["A"].extend("DD")
            maze["B"].extend("CB")
            maze["C"].extend("BA")
            maze["D"].extend("AC")
    return maze


def part_one(data: str) -> int:
    allocations = parse_maze(data)
    maze = Maze.from_allocations(allocations)
    return solve(maze, 0)


def part_two(data: str) -> int:
    allocations = parse_maze(data, unfolded=True)
    maze = Maze.from_allocations(allocations)
    return solve(maze, 0)


def test():
    test_input = """#############
#..2......9.#
###B#C#B#D###
  #A#D#C#A#
  #########"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 12521, answer_1
    assert answer_2 == 44169, answer_2


if __name__ == "__main__":
    # test()
    data = aocd.get_data(day=23, year=2021)
    # print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
