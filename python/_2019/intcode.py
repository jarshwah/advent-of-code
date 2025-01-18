import contextlib
import itertools
from collections import deque
from collections.abc import Callable, Iterator
from copy import deepcopy
from dataclasses import dataclass, field
from enum import IntEnum, unique
from functools import cache
from typing import Any, Iterable, Self, assert_never


class Halt(Exception):
    pass


class BadOpcode(Exception):
    pass


class SegFault(Exception):
    pass


class InvalidParam(Exception):
    pass


class NoInput(Exception):
    pass


type Pointer = int


@dataclass
class Memory:
    mem: dict[int, int]

    def read(self, ptr: Pointer) -> int:
        if ptr < 0:
            raise SegFault(f"Read: {ptr=} < 0")

        return self.mem.setdefault(ptr, 0)

    def write(self, ptr: Pointer, val: int) -> None:
        try:
            self.mem[ptr] = val
        except IndexError as ex:
            raise SegFault(f"Write: {ptr=} >= {self.size=}") from ex

    @property
    def size(self) -> int:
        return len(self.mem)

    def dump(self) -> list[int]:
        mem = []
        for key in sorted(self.mem.keys()):
            mem.append(self.mem[key])
        return mem


@unique
class OpCode(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JMP1 = 5
    JMP0 = 6
    LT = 7
    EQ = 8
    RELBASE = 9
    HALT = 99


@unique
class ParamMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


@dataclass
class Param:
    pointer: Pointer
    mode: ParamMode

    def resolve(self, memory: Memory, relative_base: int) -> int:
        match self.mode:
            case ParamMode.POSITION:
                return memory.read(self.pointer)

            case ParamMode.IMMEDIATE:
                return self.pointer

            case ParamMode.RELATIVE:
                return memory.read(self.pointer) + relative_base

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

    def visit(self, intcode: "IntCode") -> int:
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

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = memory.read(self.params[0].resolve(memory, intcode.relative_base))
        p2 = memory.read(self.params[1].resolve(memory, intcode.relative_base))
        p3 = self.params[2].resolve(memory, intcode.relative_base)
        memory.write(p3, p1 + p2)
        return intcode.ptr + 4


class InstructionMul(Instruction):
    opcode: OpCode = OpCode.MUL
    arity: int = 3

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = memory.read(self.params[0].resolve(memory, intcode.relative_base))
        p2 = memory.read(self.params[1].resolve(memory, intcode.relative_base))
        p3 = self.params[2].resolve(memory, intcode.relative_base)
        memory.write(p3, p1 * p2)
        return intcode.ptr + 4


class InstructionHalt(Instruction):
    opcode: OpCode = OpCode.HALT
    arity: int = 0

    def visit(self, intcode: "IntCode") -> int:
        raise Halt


class InstructionInput(Instruction):
    opcode: OpCode = OpCode.INPUT
    arity: int = 1

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = self.params[0].resolve(memory, intcode.relative_base)
        memory.write(p1, next(intcode.input))
        return intcode.ptr + 2


class InstructionOutput(Instruction):
    opcode: OpCode = OpCode.OUTPUT
    arity: int = 1

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = memory.read(self.params[0].resolve(memory, intcode.relative_base))
        intcode.output.write(p1)
        return intcode.ptr + 2


class InstructionJmp1(Instruction):
    opcode: OpCode = OpCode.JMP1
    arity: int = 2

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = memory.read(self.params[0].resolve(memory, intcode.relative_base))
        if p1 != 0:
            return memory.read(self.params[1].resolve(memory, intcode.relative_base))
        return intcode.ptr + 3


class InstructionJmp0(Instruction):
    opcode: OpCode = OpCode.JMP0
    arity: int = 2

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = memory.read(self.params[0].resolve(memory, intcode.relative_base))
        if p1 == 0:
            return memory.read(self.params[1].resolve(memory, intcode.relative_base))
        return intcode.ptr + 3


class InstructionLt(Instruction):
    opcode: OpCode = OpCode.LT
    arity: int = 3

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = memory.read(self.params[0].resolve(memory, intcode.relative_base))
        p2 = memory.read(self.params[1].resolve(memory, intcode.relative_base))
        p3 = self.params[2].resolve(memory, intcode.relative_base)
        memory.write(p3, int(p1 < p2))
        return intcode.ptr + 4


class InstructionEq(Instruction):
    opcode: OpCode = OpCode.EQ
    arity: int = 3

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = memory.read(self.params[0].resolve(memory, intcode.relative_base))
        p2 = memory.read(self.params[1].resolve(memory, intcode.relative_base))
        p3 = self.params[2].resolve(memory, intcode.relative_base)
        memory.write(p3, int(p1 == p2))
        return intcode.ptr + 4


class InstructionRelBase(Instruction):
    opcode: OpCode = OpCode.RELBASE
    arity: int = 1

    def visit(self, intcode: "IntCode") -> int:
        memory = intcode.memory
        p1 = memory.read(self.params[0].resolve(memory, intcode.relative_base))
        intcode.relative_base += p1
        return intcode.ptr + 2


@dataclass
class Pipe:
    """
    An [I]nput[O]utput Pipe.

    Callbacks can be registered to run when output is written or input is requested.
    """

    _queue: deque[int] = field(default_factory=lambda: deque([]))
    _fill_pipe: Callable[[], Any] = field(default_factory=lambda: lambda: None, repr=False)
    _pipe_filled: Callable[[], Any] = field(default_factory=lambda: lambda: None, repr=False)

    @classmethod
    def create(cls, input: list[int]) -> Self:
        return cls(_queue=deque(input))

    def __next__(self) -> int:
        if not self._queue:
            self._fill_pipe()  # request input
            if not self._queue:
                raise NoInput
        return self._queue.popleft()

    def write(self, value: int) -> None:
        self._queue.append(value)
        self._pipe_filled()

    def dump(self) -> list[int]:
        return list(self._queue)


@dataclass
class IntCode:
    _program: list[int] = field(repr=False)
    ptr: Pointer = 0
    input: Pipe = field(default_factory=Pipe)
    output: Pipe = field(default_factory=Pipe)
    _halted: bool = False
    _executing: bool = False
    relative_base: int = 0
    name: str = ""
    _memory: Memory = field(init=False)

    def __post_init__(self) -> None:
        self._memory = Memory({idx: mem for idx, mem in enumerate(self._program)})
        self.output._fill_pipe = self.run
        self.input._pipe_filled = self.run

    @property
    def memory(self) -> Memory:
        return self._memory

    def decode_instruction(self, ptr: Pointer) -> Instruction:
        raw = str(self.memory.read(ptr))[::-1]
        opcode = int(raw[:2][::-1])
        raw_modes = raw[2:]
        modes = (ParamMode(int(mode)) for mode in raw_modes)
        args = (ptr, modes)
        return get_instruction_type(opcode).build(*args)

    def run(self) -> list[int]:
        """Run all instructions until the program halts"""
        if self._halted or self._executing:
            return self.output.dump()

        while True:
            try:
                self.next()
            except Halt:
                self._halted = True
                return self.output.dump()
            except NoInput:
                # Pause, allowing resumption when input is provided.
                return []

    def next(self) -> None:
        inst = self.decode_instruction(self.ptr)
        with self.executing():
            self.ptr = inst.visit(self)

    @contextlib.contextmanager
    def executing(self) -> Iterator[None]:
        """Mark the interpreter as executing to prevent re-entrant calls"""
        try:
            self._executing = True
            yield
        finally:
            self._executing = False

    def connect_input(self, other: "IntCode") -> None:
        self.input = other.output
        self.input._pipe_filled = self.run

    def fork(self) -> Self:
        forked = deepcopy(self)
        forked.output._fill_pipe = forked.run
        forked.input._pipe_filled = forked.run
        return forked


@cache
def get_instruction_type(opcode: int) -> type[Instruction]:
    for inst in Instruction.__subclasses__():
        if inst.opcode == opcode:
            return inst
    raise BadOpcode(f"{opcode=}")


def chain_intcode_io(*intcodes: IntCode, loop: bool = False) -> None:
    """
    Chain intcode outputs to inputs.

    Optionally link the final output to the first input when loop is True.
    """
    for r1, r2 in zip(intcodes, intcodes[1:]):
        r2.connect_input(r1)
    if loop:
        intcodes[0].connect_input(intcodes[-1])
