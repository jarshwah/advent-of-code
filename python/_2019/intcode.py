import itertools
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum, unique
from functools import cached_property
from typing import Iterable, Self, assert_never


class Halt(Exception):
    pass


class BadOpcode(Exception):
    pass


class SegFault(Exception):
    pass


class InvalidParam(Exception):
    pass


type Operation = Callable[[int, int], int]
type Pointer = int


@dataclass
class Memory:
    mem: list[int]

    def read(self, ptr: Pointer) -> int:
        try:
            return self.mem[ptr]
        except IndexError as ex:
            raise SegFault(f"Read: {ptr=} >= {self.size=}") from ex

    def write(self, ptr: Pointer, val: int) -> None:
        try:
            self.mem[ptr] = val
        except IndexError as ex:
            raise SegFault(f"Write: {ptr=} >= {self.size=}") from ex

    @property
    def size(self) -> int:
        return len(self.mem)


@unique
class OpCode(IntEnum):
    ADD = 1
    MUL = 2
    HALT = 99


@unique
class ParamMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1


@dataclass
class Param:
    pointer: Pointer
    mode: ParamMode

    def resolve(self, memory: Memory) -> int:
        match self.mode:
            case ParamMode.POSITION:
                return memory.read(self.pointer)

            case ParamMode.IMMEDIATE:
                return self.pointer

            case _:
                assert_never(self.mode)


@dataclass
class Instruction:
    opcode: OpCode
    arity: int
    params: list[Param]

    def __post_init__(self) -> None:
        assert len(self.params) == self.arity, "Length of params does not match arity"

    def __len__(self) -> int:
        return self.arity + 1

    def visit(self, memory: Memory) -> None:
        raise NotImplementedError

    @classmethod
    def build(cls, ptr: Pointer, modes: Iterable[ParamMode]) -> Self:
        return cls(
            opcode=cls.opcode,
            arity=cls.arity,
            params=[
                Param(ptr + ptrn, mode)
                for ptrn, mode in zip(
                    range(1, cls.arity + 1),
                    itertools.chain(modes, itertools.repeat(ParamMode.POSITION)),
                )
            ],
        )


class InstructionAdd(Instruction):
    opcode: OpCode = OpCode.ADD
    arity: int = 3

    def visit(self, memory: Memory) -> None:
        p1 = memory.read(self.params[0].resolve(memory))
        p2 = memory.read(self.params[1].resolve(memory))
        p3 = self.params[2].resolve(memory)
        memory.write(p3, p1 + p2)


class InstructionMul(Instruction):
    opcode: OpCode = OpCode.MUL
    arity: int = 3

    def visit(self, memory: Memory) -> None:
        p1 = memory.read(self.params[0].resolve(memory))
        p2 = memory.read(self.params[1].resolve(memory))
        p3 = self.params[2].resolve(memory)
        memory.write(p3, p1 * p2)


class InstructionHalt(Instruction):
    opcode: OpCode = OpCode.HALT
    arity: int = 0

    def visit(self, memory: Memory) -> None:
        raise Halt


@dataclass
class IntCode:
    _memory: list[int]
    ptr: Pointer = 0

    @cached_property
    def memory(self) -> Memory:
        return Memory(self._memory)

    def decode_instruction(self, ptr: Pointer) -> Instruction:
        raw = str(self.memory.read(ptr))[::-1]
        opcode = int(raw[:2][::-1])
        raw_modes = raw[2:]
        modes = (ParamMode(int(mode)) for mode in raw_modes)
        args = (ptr, modes)
        match opcode:
            case OpCode.ADD:
                return InstructionAdd.build(*args)
            case OpCode.MUL:
                return InstructionMul.build(*args)
            case OpCode.HALT:
                return InstructionHalt.build(*args)
            case _:
                raise BadOpcode(f"{opcode=} {ptr=}")

    def run(self) -> None:
        """Run all instructions until the program halts"""
        while True:
            try:
                self.next()
            except Halt:
                return

    def next(self) -> None:
        inst = self.decode_instruction(self.ptr)
        inst.visit(self.memory)
        self.advance(len(inst))

    def advance(self, n: int) -> None:
        """Advance pointer n steps."""
        self.ptr += n
