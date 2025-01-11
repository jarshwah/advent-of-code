import pytest

from . import intcode
from .intcode import IntCode, Pipe


class TestInstructionAdd:
    def test_add_positional(self):
        inst = intcode.InstructionAdd.build(
            ptr=0, modes=[intcode.ParamMode.POSITION, intcode.ParamMode.POSITION]
        )
        ic = IntCode([intcode.OpCode.ADD, 3, 4, 1, 7])
        inst.visit(ic)
        assert ic.memory.read(1) == 8


class TestInstructionMul:
    def test_mul_positional(self):
        inst = intcode.InstructionMul.build(
            ptr=0, modes=[intcode.ParamMode.POSITION, intcode.ParamMode.POSITION]
        )
        ic = IntCode([intcode.OpCode.ADD, 3, 4, 1, 7])
        inst.visit(ic)
        assert ic.memory.read(1) == 7


class TestInstructionHalt:
    def test_hal(self):
        inst = intcode.InstructionHalt.build(
            ptr=0, modes=[intcode.ParamMode.POSITION, intcode.ParamMode.POSITION]
        )
        ic = intcode.IntCode([intcode.OpCode.HALT, 3, 4, 1, 7])
        with pytest.raises(intcode.Halt):
            inst.visit(ic)


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
        ([1101, 100, -1, 4, 0], [1101, 100, -1, 4, 99]),
    ],
)
def test_run(incodes: list[int], outcodes: list[int]):
    program = IntCode(incodes)
    program.run()
    assert program._memory == outcodes


class TestIntCode:
    def test_outputs_input(self):
        """Day 5: program outputs the input"""
        program = IntCode([3, 0, 4, 0, 99], input=Pipe.create([-4]))
        program.run()
        assert program.output.dump() == [-4]

    @pytest.mark.parametrize(
        "mem,input,result",
        [
            # eq 8 - 1
            ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8], [1]),
            ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8], [1]),
            # eq 8 - 0
            ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [6], [0]),
            ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [6], [0]),
            # lt 8 - 1
            ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [7], [1]),
            ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [7], [1]),
            # lt 8 - 0
            ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8], [0]),
            ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8], [0]),
        ],
    )
    def test_input_eq_lt(self, mem, input, result):
        program = IntCode(mem, input=Pipe.create(input))
        program.run()
        assert program.output.dump() == result

    @pytest.mark.parametrize(
        "mem,input,result",
        [
            ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0], [0]),
            ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0], [0]),
            ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [5], [1]),
            ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [5], [1]),
        ],
    )
    def test_jmp(self, mem, input, result):
        program = IntCode(mem, input=Pipe.create(input))
        program.run()
        assert program.output.dump() == result

    def test_day5(self):
        # fmt: off
        mem = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
        # fmt: on
        program = IntCode(mem, input=Pipe.create([7]))
        program.run()
        assert program.output.dump() == [999]

        program = IntCode(mem, input=Pipe.create([8]))
        program.run()
        assert program.output.dump() == [1000]

        program = IntCode(mem, input=Pipe.create([9]))
        program.run()
        assert program.output.dump() == [1001]

    def test_io_chain_looped_shares_io(self):
        r1 = IntCode([])
        r2 = IntCode([])
        intcode.chain_intcode_io(r1, r2, loop=True)
        assert r1.output == r2.input
        assert r2.output == r1.input

    def test_io_chain_unlooped_shares_io(self):
        r1 = IntCode([])
        r2 = IntCode([])
        intcode.chain_intcode_io(r1, r2, loop=False)
        assert r1.output == r2.input
        assert r2.output != r1.input

    def test_io_chain_looped_propagates_io(self):
        # write input to 3, then * 2, then write back to output, then halt.
        # fmt: off
        r1 = IntCode(
            [
                intcode.OpCode.INPUT,  # Read INPUT from R2 OUTPUT (7)
                3,
                1102,                  # MUL IMMEDIATE (7 * 2)
                0,                     # Result of INPUT (7)
                2,                     # * 2
                3,                     # Write back to Result of INPUT
                intcode.OpCode.OUTPUT, # Then output it again
                3,                     # 14 was stored at [3]
                intcode.OpCode.HALT,   # and exit
            ],
            name="R1"
        )
        # fmt: on

        # Take STDIN, write it to R1 via Output stream, which will multiply by 2
        # and write to our Input stream, then we place it onto our Output stream.

        # fmt: off
        r2 = IntCode(
            [
                intcode.OpCode.INPUT,  # Read INPUT from stdin
                3,                     # Write it to JMP compare
                intcode.OpCode.JMP0,   # If Input is 0, JMP to halt
                0,
                8,
                intcode.OpCode.OUTPUT, # Otherwise, Write 7 [3] to OUTPUT
                3,
                intcode.OpCode.INPUT,  # Then receive from r1
                6,
                intcode.OpCode.OUTPUT, # And OUTPUT the r1 input
                6,
                intcode.OpCode.HALT,   # and exit
            ],
            name="R2"
        )
        # fmt: on

        intcode.chain_intcode_io(r1, r2, loop=True)
        r2.input.write(7)  # stdin
        r2.run()  # 7 * 2 back to output
        assert r2.output.dump() == [14]
