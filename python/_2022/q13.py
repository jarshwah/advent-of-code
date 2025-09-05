import itertools
from ast import literal_eval
from functools import cmp_to_key
import utils
from utils import first


def compare_recursive(left: RecursiveInt, right: RecursiveInt) -> int:
    match (left, right):
        case (int(left), int(right)):
            return left - right
        case (list(left), list(right)):
            return first(
                [r for z in zip(left, right) if (r := compare_recursive(*z))]
                + [len(left) - len(right)]
            )
        case (int(left), list(right)):
            return compare_recursive([left], right)
        case (list(left), int(right)):
            return compare_recursive(left, [right])


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        return sum(
            pair_num
            for pair_num, pair in enumerate(utils.Input.group("\n\n", sep="\n").strings, 1)
            if compare_recursive(literal_eval(pair[0]), literal_eval(pair[1])) < 0
        )

    def part_two(self, input: utils.Input) -> str | int:
        packets = [
            (literal_eval(pair[0]), literal_eval(pair[1]))
            for pair in utils.Input.group("\n\n", sep="\n").strings
        ] + [([[2]], [[6]])]
        sorted_packets = sorted(
            itertools.chain.from_iterable(packets), key=cmp_to_key(compare_recursive)
        )

        return (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)


puzzle = Puzzle(
    year=2022,
    day=13,
    test_answers=("13", "140"),
    test_input="""\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""",
)

if __name__ == "__main__":
    puzzle.cli()
