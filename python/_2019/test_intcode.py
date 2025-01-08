import pytest

from . import intcode
from .intcode import IntCode


class TestInstructionAdd:
    def test_add_positional(self):
        inst = intcode.InstructionAdd.build(
            ptr=0, modes=[intcode.ParamMode.POSITION, intcode.ParamMode.POSITION]
        )
        mem = intcode.Memory([intcode.OpCode.ADD, 3, 4, 1, 7])
        inst.visit(mem)
        assert mem.read(1) == 8


class TestInstructionMul:
    def test_mul_positional(self):
        inst = intcode.InstructionMul.build(
            ptr=0, modes=[intcode.ParamMode.POSITION, intcode.ParamMode.POSITION]
        )
        mem = intcode.Memory([intcode.OpCode.ADD, 3, 4, 1, 7])
        inst.visit(mem)
        assert mem.read(1) == 7


class TestInstructionHalt:
    def test_hal(self):
        inst = intcode.InstructionHalt.build(
            ptr=0, modes=[intcode.ParamMode.POSITION, intcode.ParamMode.POSITION]
        )
        mem = intcode.Memory([intcode.OpCode.HALT, 3, 4, 1, 7])
        with pytest.raises(intcode.Halt):
            inst.visit(mem)


def test_add():
    """
    ADD instruction will add 1 + 7 (position 3 and position 4) and assign to position 1
    """
    program = IntCode([intcode.OpCode.ADD, 3, 4, 1, 7])
    program.next()
    assert program.memory.read(1) == 8


def test_mul():
    """
    MUL instruction will multiply 1 + 7 (position 3 and position 4) and assign to position 1
    """
    program = IntCode([intcode.OpCode.MUL, 3, 4, 1, 7])
    program.next()
    assert program.memory.read(1) == 7


def test_halt():
    """
    HALT immediately exits the program.
    """
    program = IntCode([intcode.OpCode.HALT, 1, 1, 1])
    with pytest.raises(intcode.Halt):
        program.next()


def test_badopcode():
    """
    UNKNOWN opcode throws an error.
    """
    program = IntCode([77, 1, 1, 1])
    with pytest.raises(intcode.BadOpcode):
        program.next()


@pytest.mark.parametrize(
    "incodes, outcodes",
    [
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
    ],
)
def test_run(incodes: list[int], outcodes: list[int]):
    program = IntCode(incodes)
    program.run()
    assert program._memory == outcodes
