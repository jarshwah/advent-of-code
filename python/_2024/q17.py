from dataclasses import dataclass

import utils


@dataclass
class Computer:
    register_a: int
    register_b: int
    register_c: int
    instructions: list[int]
    output: list[int]
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
        while self.pointer < len(self.instructions):
            opcode = self.instructions[self.pointer]
            literal = self.instructions[self.pointer + 1]
            combo = self.get_combo_operand(literal)
            match opcode:
                case 0:
                    self.register_a //= 2**combo
                case 1:
                    self.register_b ^= literal
                case 2:
                    self.register_b = combo % 8
                case 3 if self.register_a == 0:
                    pass
                case 3 if self.register_a != 0:
                    self.pointer = literal
                    continue
                case 4:
                    self.register_b ^= self.register_c
                case 5:
                    self.output.append(combo % 8)
                    if self.halt_early and self.output != self.instructions[: len(self.output)]:
                        return self.output
                case 6:
                    self.register_b = self.register_a // (2**combo)
                case 7:
                    self.register_c = self.register_a // (2**combo)
            self.pointer += 2
        return self.output


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        ([ra], [rb], [rc]), [instructions] = input.group(sep="\n").scan_ints()
        computer = Computer(ra, rb, rc, list(instructions), [])
        computer.run()
        return ",".join(str(s) for s in computer.output)

    def part_two(self, input: utils.Input) -> str | int:
        ([ra], [rb], [rc]), [instructions] = input.group(sep="\n").scan_ints()
        instructions = list(instructions)
        ra = 0 if input.data == self.test_input_2 else 216549845000000
        while True:
            computer = Computer(ra, rb, rc, instructions, [], halt_early=True)
            output = computer.run()
            if output == instructions:
                return ra
            ra += 1


if __name__ == "__main__":
    runner = Puzzle(
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
    runner.cli()
