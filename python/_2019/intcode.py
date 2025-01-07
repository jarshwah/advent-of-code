import operator
from collections.abc import Callable
from dataclasses import dataclass


class Halt(Exception):
    pass


class BadOpcode(Exception):
    pass


class SegFault(Exception):
    pass


type Output = int
type Operation = Callable[[int, int], int]


@dataclass
class IntCode:
    memory: list[int]
    ptr: int = 0

    def run(self) -> None:
        """Run all instructions until the program halts"""
        while True:
            try:
                self.next()
            except Halt:
                return

    def next(self) -> None:
        opcode = self.memory[self.ptr]
        match opcode:
            case 1:
                self.add()
                self.advance(4)
            case 2:
                self.mul()
                self.advance(4)
            case 99:
                self.halt()
            case _:
                raise BadOpcode(f"{opcode=} {self.ptr=}")

    def advance(self, n: int) -> None:
        """Advance pointer n steps."""
        self.ptr += n
        if self.ptr >= len(self.memory):
            raise SegFault(f"Advance: {self.ptr=} >= {len(self.memory)=}")

    def deref(self, ptr: int) -> int:
        """Return the value at the position the pointer points at"""
        try:
            ref_ptr = self.ref(ptr)
            return self.memory[ref_ptr]
        except IndexError as ex:
            raise SegFault(f"Deref: {ref_ptr=} >= {len(self.memory)=}") from ex

    def ref(self, ptr: int) -> int:
        """Return the position the pointer points at"""
        try:
            return self.memory[ptr]
        except IndexError as ex:
            raise SegFault(f"Ref: {ptr=} >= {len(self.memory)=}") from ex

    def add(self) -> int:
        """opcode 1"""
        return self._op(operator.add)

    def mul(self) -> int:
        """opcode 2"""
        return self._op(operator.mul)

    def halt(self) -> None:
        """opcode 99"""
        raise Halt

    def _op(self, operation: Operation) -> int:
        """
        Applies an operator to arg1 and arg2 assigning it to target and returning the result.

        ptr + 1 = position of arg1
        ptr + 2 = position of arg2
        ptr + 3 = position of target
        """
        address = self.ref(self.ptr + 3)
        val = operation(self.deref(self.ptr + 1), self.deref(self.ptr + 2))
        self._assign(address, val)
        return val

    def _assign(self, address: int, value: int) -> None:
        try:
            self.memory[address] = value
        except IndexError as ex:
            raise SegFault(f"Assign: {address=} >= {len(self.memory)=}") from ex
