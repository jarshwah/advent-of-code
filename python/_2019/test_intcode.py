import pytest

from . import intcode
from .intcode import IntCode

ADD = 1
MUL = 2
HALT = 99


def test_add():
    """
    ADD instruction will add 1 + 7 (position 3 and position 4) and assign to position 1
    """
    program = IntCode([ADD, 3, 4, 1, 7])
    program.next()
    assert program.memory[1] == 8


def test_mul():
    """
    MUL instruction will multiply 1 + 7 (position 3 and position 4) and assign to position 1
    """
    program = IntCode([MUL, 3, 4, 1, 7])
    program.next()
    assert program.memory[1] == 7


def test_halt():
    """
    HALT immediately exits the program.
    """
    program = IntCode([HALT, 1, 1, 1])
    with pytest.raises(intcode.Halt):
        program.next()


def test_badopcode():
    """
    UNKNOWN opcode throws an error.
    """
    program = IntCode([999, 1, 1, 1])
    with pytest.raises(intcode.BadOpcode):
        program.next()


@pytest.mark.parametrize(
    "incodes, outcodes",
    [
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ],
)
def test_run(incodes: list[int], outcodes: list[int]):
    program = IntCode(incodes)
    program.run()
    assert program.memory == outcodes
