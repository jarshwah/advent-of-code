from typing import Sequence

import utils


def is_safe(nums: Sequence[int], low: int, high: int) -> bool:
    """
    A report is safe if it's always increasing or always decreasing within the range.

    ie [1, 2, 3, 4, 5] is safe with low=1, high=3
    ie [5, 4, 3, 2, 1] is safe with low=1, high=3
    ie [1, 2, 3, 2, 1] is not safe with low=1, high=3
    """
    diffs = [left - right for left, right in zip(nums, nums[1:])]
    same_direction = all(d < 0 for d in diffs) or all(d > 0 for d in diffs)
    within_tolerance = all(low <= abs(d) <= high for d in diffs)
    return same_direction and within_tolerance


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """Find all safe reports."""
        reports = input.lines().split().numbers
        return sum(is_safe(report, 1, 3) for report in reports)

    def part_two(self, input: utils.Input) -> str | int:
        """Find all safe reports with an optional missing number."""
        reports = input.lines().split().numbers
        return sum(
            any(is_safe(list(report[:i]) + list(report[i + 1 :]), 1, 3) for i in range(len(report)))
            for report in reports
        )


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=2,
        test_answers=("2", "4"),
        test_input="""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""",
    )
    runner.cli()
