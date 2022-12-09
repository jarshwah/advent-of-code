import aocd
import utils


def solve(raw: str, knots: int) -> int:
    instructions = utils.Input(raw).split("\n").strings
    rope = [(0, 0)] * knots
    visited = {rope[-1]}
    for instruction in instructions:
        direction, count = instruction.split()
        for _ in range(int(count)):
            head = rope[0]
            match direction:
                case "U":
                    head = utils.sum_points(head, utils.UP)
                case "D":
                    head = utils.sum_points(head, utils.DOWN)
                case "L":
                    head = utils.sum_points(head, utils.LEFT)
                case "R":
                    head = utils.sum_points(head, utils.RIGHT)
                case _:
                    raise ValueError(direction)
            rope[0] = head
            for pos, ht in enumerate(zip(rope, rope[1:]), 1):
                (hr, hc), (tr, tc) = ht
                while max(abs(hr - tr), abs(hc - tc)) > 1:
                    if abs(hr - tr) > 0:
                        tr += 1 if hr > tr else -1
                    if abs(hc - tc) > 0:
                        tc += 1 if hc > tc else -1
                rope[pos] = tr, tc
            visited.add(rope[-1])
    return len(visited)


def test():
    test_input = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
    answer_1 = solve(test_input, knots=2)
    answer_2 = solve(test_input, knots=10)
    assert answer_1 == 88, answer_1
    assert answer_2 == 36, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=9, year=2022)
    print("Part 1: ", solve(data, knots=2))
    print("Part 2: ", solve(data, knots=10))
