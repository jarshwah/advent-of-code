from __future__ import annotations

from dataclasses import dataclass
import typing as t
import aocd
from enum import Enum

from parse import compile


parser = compile("{opcode} {num:d}")


class OpCode(str, Enum):
    nop = "nop"
    acc = "acc"
    jmp = "jmp"

    def flip(self) -> OpCode:
        if self == OpCode.nop:
            return OpCode.jmp
        if self == OpCode.jmp:
            return OpCode.nop
        return OpCode.acc


@dataclass(eq=True)
class Instruction:
    opcode: OpCode
    num: int

    def __init__(self, opcode: str, num: int):
        self.opcode = OpCode[opcode]
        self.num = num

    def execute(self, pointer: int, acc: int) -> t.Tuple[int, int]:
        return self._exec(pointer, acc, self.opcode, self.num)

    def rewind(self, pointer: int, acc: int) -> t.Tuple[int, int]:
        return self._exec(pointer, acc, self.opcode, -self.num)

    def flipped(self) -> Instruction:
        if self.opcode is OpCode.acc:
            return self
        return Instruction(self.opcode.flip().value, self.num)

    def _exec(self, pointer: int, acc: int, opcode: OpCode, num: int) -> t.Tuple[int, int]:
        if opcode == OpCode.nop:
            return pointer + 1, acc
        elif opcode == OpCode.acc:
            return pointer + 1, acc + num
        elif opcode == OpCode.jmp:
            return pointer + num, acc
        raise ValueError


@dataclass
class Frame:
    pointer: int
    acc: int
    seen: t.Set


def part_one(instructions: t.List[Instruction]) -> int:
    seen = set()
    acc = pointer = 0
    while pointer not in seen:
        seen.add(pointer)
        pointer, acc = instructions[pointer].execute(pointer, acc)
    return acc


def part_two(instructions: t.List[Instruction]) -> int:
    seen = set()
    acc = pointer = 0
    flip_back = -1
    stack: t.List[Frame] = []
    while pointer < len(instructions):
        if pointer in seen:
            if flip_back >= 0:
                # flipping this didn't work, so restore to original state
                instruction = instructions[flip_back]
                instructions[flip_back] = instruction.flipped()

            frame = stack.pop()
            seen = frame.seen
            acc = frame.acc
            pointer = frame.pointer
            instruction = instructions[pointer].flipped()
            flip_back = pointer
        instruction = instructions[pointer]
        seen.add(pointer)
        pointer, acc = instruction.execute(pointer, acc)
        if flip_back < 0:
            # Only save frames on the way down, not back up
            stack.append(Frame(pointer, acc, seen.copy()))
    return acc


if __name__ == "__main__":
    instructions: t.List[Instruction] = [
        Instruction(**parser.search(instruction).named)
        for instruction in aocd.get_data(day=8, year=2020).splitlines()
    ]
    print("Part 1: ", part_one(instructions))
    print("Part 2: ", part_two(instructions))
