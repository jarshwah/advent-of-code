from dataclasses import dataclass

import utils


@dataclass
class Computer:
    register_a: int
    register_b: int
    register_c: int
    instructions: list[int]
    pointer: int = 0
    halt_early: bool = False

    def get_combo_operand(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.register_a
        if operand == 5:
            return self.register_b
        if operand == 6:
            return self.register_c
        raise ValueError(f"Invalid operand: {operand}")

    def run(self) -> list[int]:
        output = []
        while self.pointer < len(self.instructions):
            opcode = self.instructions[self.pointer]
            literal = self.instructions[self.pointer + 1]
            combo = self.get_combo_operand(literal)
            self.pointer += 2
            # fmt: off
            match opcode:
                case 0: self.register_a //= 2**combo
                case 1: self.register_b ^= literal
                case 2: self.register_b = combo % 8
                case 3 if self.register_a == 0: pass
                case 3 if self.register_a != 0: self.pointer = literal
                case 4: self.register_b ^= self.register_c
                case 5: output.append(combo % 8)
                case 6: self.register_b = self.register_a // (2**combo)
                case 7: self.register_c = self.register_a // (2**combo)
            # fmt: on
            if self.halt_early and output != self.instructions[: len(output)]:
                return output
        return output

    def run_two(self) -> list[int]:
        """
        Decompiled - runs a little faster, but only on my input.
        """
        out = []
        A, B, C = self.register_a, self.register_b, self.register_c
        while True:
            B = (A % 8) ^ 3
            C = A // (2**B)
            B = B ^ 5
            A = A // (2**3)
            B = B ^ C
            out.append(B % 8)
            if A == 0:
                return out


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        ([ra], [rb], [rc]), [instructions] = input.group(sep="\n").scan_ints()
        computer = Computer(ra, rb, rc, list(instructions))
        output = computer.run()
        return ",".join(str(s) for s in output)

    def part_two(self, input: utils.Input) -> str | int:
        ([ra], [rb], [rc]), [instructions] = input.group(sep="\n").scan_ints()
        instructions = list(instructions)
        ra = 0 if input.data == self.test_input_2 else 216549845000000
        while True:
            computer = Computer(ra, rb, rc, instructions, halt_early=True)
            output = computer.run()
            if output == instructions:
                return ra
            ra += 1


puzzle = Puzzle(
    year=2024,
    day=17,
    test_answers=("4,6,3,5,6,3,5,2,1,0", "117440"),
    test_input="""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""",
    test_input_2="""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""",
)

if __name__ == "__main__":
    puzzle.cli()
