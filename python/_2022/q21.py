import z3
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        data = input.string.splitlines()
        solver = z3.Optimize()
        terms = {}
        for line in data:
            monkey, equation = line.split(":")
            parts = equation.strip().split(" ")
            match parts:
                case [num]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    n = int(num)
                    solver.add(term == n)
                case [m1, "+", m2]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(term == (m1 + m2))
                case [m1, "-", m2]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(term == (m1 - m2))
                case [m1, "*", m2]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(term == (m1 * m2))
                case [m1, "/", m2]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(term == (m1 / m2))

        root = terms["root"]
        solver.check()
        model = solver.model()
        return model[root].as_long()

    def part_two(self, input: utils.Input) -> str | int:
        data = input.string.splitlines()
        solver = z3.Optimize()
        terms = {}
        for line in data:
            monkey, equation = line.split(":")
            parts = equation.strip().split(" ")
            match parts:
                case [num] if monkey == "humn":
                    term = terms.setdefault(monkey, z3.Int(monkey))
                case [num]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    n = int(num)
                    solver.add(term == n)
                case [m1, "+", m2] if monkey == "root":
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(m1 == m2)
                case [m1, "+", m2]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(term == (m1 + m2))
                case [m1, "-", m2]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(term == (m1 - m2))
                case [m1, "*", m2]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(term == (m1 * m2))
                case [m1, "/", m2]:
                    term = terms.setdefault(monkey, z3.Int(monkey))
                    m1 = terms.setdefault(m1, z3.Int(m1))
                    m2 = terms.setdefault(m2, z3.Int(m2))
                    solver.add(term == (m1 / m2))

        humn = terms["humn"]
        solver.check()
        model = solver.model()

        return model[humn].as_long()


puzzle = Puzzle(
    year=2022,
    day=21,
    test_answers=("152", "301"),
    test_input="""\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""",
)

if __name__ == "__main__":
    puzzle.cli()
