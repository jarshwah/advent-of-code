import parse
import utils


def stackem(raw: str) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    parts = raw.split("\n\n")
    crates = parts[0].split("\n")
    instructions = parts[1].split("\n")
    # Each square is 4 spaces, except the last, so add 1 (could use ceil)
    stacks: list[list[str]] = [[] for _ in range(len(crates[0]) // 4 + 1)]
    for row in reversed(crates[:-1]):
        for stack_num, letter in enumerate(row[1::4]):
            if letter := letter.strip():
                stacks[stack_num].append(letter)
    work_order = [parse.parse("move {:d} from {:d} to {:d}", row) for row in instructions]

    return stacks, work_order


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        stacks, work_order = stackem(input.string)
        for num, source, target in work_order:
            for _ in range(num):
                stacks[target - 1].append(stacks[source - 1].pop())
        return "".join([stack[-1] for stack in stacks if stack])

    def part_two(self, input: utils.Input) -> str | int:
        stacks, work_order = stackem(input.string)
        for num, source, target in work_order:
            picked = reversed([stacks[source - 1].pop() for _ in range(num)])
            stacks[target - 1].extend(picked)
        return "".join([stack[-1] for stack in stacks if stack])


puzzle = Puzzle(
    year=2022,
    day=5,
    test_answers=("CMZ", "MCD"),
    test_input="""    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""",
)

if __name__ == "__main__":
    puzzle.cli()
