import aocd
import parse
import utils


def stackem(raw: str) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    crates, instructions = utils.Input(raw).split("\n\n").split("\n").strings
    # Each square is 4 spaces, except the last, so add 1 (could use ceil)
    stacks: list[list[str]] = [[] for _ in range(len(crates[0]) // 4 + 1)]
    for row in reversed(crates[:-1]):
        for stack_num, letter in enumerate(row[1::4]):
            if letter := letter.strip():
                stacks[stack_num].append(letter)
    work_order = [parse.parse("move {:d} from {:d} to {:d}", row) for row in instructions]

    return stacks, work_order


def part_one(raw: str) -> str:
    stacks, work_order = stackem(raw)
    for num, source, target in work_order:
        for _ in range(num):
            stacks[target - 1].append(stacks[source - 1].pop())
    return "".join([stack[-1] for stack in stacks if stack])


def part_two(raw: str) -> str:
    stacks, work_order = stackem(raw)
    for num, source, target in work_order:
        picked = reversed([stacks[source - 1].pop() for _ in range(num)])
        stacks[target - 1].extend(picked)
    return "".join([stack[-1] for stack in stacks if stack])


def test():
    # fmt: off
    # my editor is chopping off trailing spaces so I'm replacing them with .
    test_input = """    [D] ...
[N] [C] ...
[Z] [M] [P]
 1   2   3.

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".replace(".", " ")
    # fmt: on
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == "CMZ", answer_1
    assert answer_2 == "MCD", answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=5, year=2022)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
