import dataclasses

import aocd
import utils


@dataclasses.dataclass(eq=True, frozen=True)
class Num:
    value: int
    position: int

    def __str__(self) -> str:
        print(self.value)


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


def test():
    test_input = """1
2
-3
3
-2
0
4"""
    answer_1 = solve(test_input, targets=[1000, 2000, 3000], key=1, iterations=1)
    answer_2 = solve(test_input, targets=[1000, 2000, 3000], key=811589153, iterations=10)

    assert answer_1 == 3, answer_1
    assert answer_2 == 1623178306, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=20, year=2022)
    print("Part 1: ", solve(data, targets=[1000, 2000, 3000], key=1, iterations=1))
    print("Part 2: ", solve(data, targets=[1000, 2000, 3000], key=811589153, iterations=10))
