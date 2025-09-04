import dataclasses
import utils


def solve(raw: str, targets: list[int], key: int, iterations: int) -> int:
    nums = [Num(val * key, idx) for idx, val in enumerate(utils.Input(raw).lines().integers)]
    other = nums[:]
    positions = len(nums)
    short = positions - 1
    zero = utils.only([n for n in nums if n.value == 0])
    for _ in range(iterations):
        for node in nums:
            curr_pos = other.index(node)
            num = other.pop(curr_pos)
            new_pos = (num.value + curr_pos) % short
            if new_pos == 0:
                new_pos = positions
            other.insert(new_pos, num)
        found = other.index(zero)
    real_targets = [(target + found) % positions for target in targets]
    return sum(other[target].value for target in real_targets)


class Puzzle(utils.Puzzle):
    pass


puzzle = Puzzle(
    year=2022,
    day=20,
    test_answers=("3", "1623178306"),
    test_input="""\
1
2
-3
3
-2
0
4""",
)

if __name__ == "__main__":
    puzzle.cli()
