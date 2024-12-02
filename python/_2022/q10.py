import aocd
import parse


def solve(raw: str) -> int:
    cycle = 0
    register = 1
    cycles = {0: register}
    for instruction in raw.splitlines():
        cycle += 1
        cycles[cycle] = register
        if found := parse.parse("addx {:d}", instruction):
            cycle += 1
            cycles[cycle] = register
            register += found[0]
    find = (20, 60, 100, 140, 180, 220)
    p1 = sum(cycles[cycle] * cycle for cycle in find)
    for i in range(240):
        x = cycles[i + 1]
        sprite = i % 40
        print("#" if x - 1 <= sprite <= x + 1 else " ", end="\n" if sprite == 39 else "")
    return p1


def test():
    test_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
    answer_1 = solve(test_input)
    assert answer_1 == 13140, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=10, year=2022)
    answer_1 = solve(data)
    print("Part 1: ", answer_1)
