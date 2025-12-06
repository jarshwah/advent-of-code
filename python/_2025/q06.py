import operator
from functools import reduce

import utils

OPS = {
    "+": operator.add,
    "*": operator.mul,
}


class Puzzle(utils.Puzzle):
    """
    --- Day 6: Trash Compactor ---
    """

    def part_one(self, input: utils.Input) -> str | int:
        """Sum all of the column-wise problems -"""
        equations = input.lines().strings
        nums = utils.transpose([[int(num) for num in row.split()] for row in equations[:-1]])
        operators = [OPS[op] for op in equations[-1].split()]
        return sum(reduce(op, nums) for op, nums in zip(operators, nums))

    def part_two(self, input: utils.Input) -> str | int:
        """Sum all of the column-wise problems with column-wise numbers"""
        equations = input.lines().strings
        num_lists = utils.transpose(equations[:-1])
        operators = (OPS[op] for op in equations[-1].split())
        total = 0
        current_operator = next(operators)
        current_nums: list[int] = []
        for num_list in num_lists:
            joined = "".join(num_list).strip()
            if not joined:
                # A list of empty nums signifies the empty column
                total += reduce(current_operator, current_nums)
                current_operator = next(operators)
                current_nums = []
                continue
            current_nums.append(int(joined))
        return total + reduce(current_operator, current_nums)


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=6,
        test_answers=("4277556", "3263827"),
        test_input="""123 328  51 64 \n 45 64  387 23 \n  6 98  215 314 \n*   +   *   +""",
    )
    runner.cli()
