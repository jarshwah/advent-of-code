import aocd
import z3


def part_one(raw: str) -> int:
    data = raw.splitlines()
    solver = z3.Solver()
    terms = {}
    for line in data:
        monkey, equation = line.split(":")
        parts = equation.strip().split(" ")
        match (parts):
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


def part_two(raw: str) -> int:
    data = raw.splitlines()
    solver = z3.Solver()
    terms = {}
    for line in data:
        monkey, equation = line.split(":")
        parts = equation.strip().split(" ")
        match (parts):
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


def test():
    test_input = """root: pppw + sjmn
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
hmdt: 32"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 152, answer_1
    assert answer_2 == 301, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=21, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
