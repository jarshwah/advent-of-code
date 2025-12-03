from collections.abc import Sequence

import utils


class Puzzle(utils.Puzzle):
    """
    Lobby.

    Find N batteries to turn on.
    Take the biggest N batteries, join them together, and sum the total.
    Batteries must be in order: 8123973 -> 97 where N is 2.
    """

    def part_one(self, input: utils.Input) -> str | int:
        return sum([self.biggest(list(map(int, bank)), 2) for bank in input.lines().strings])

    def part_two(self, input: utils.Input) -> str | int:
        return sum([self.biggest(list(map(int, bank)), 12) for bank in input.lines().strings])

    def biggest(self, bank: Sequence[int], num: int) -> int:
        output: list[int] = []
        start, end = 0, -num + 1
        for _ in range(num):
            # [slice_start: slice_end] doesn't work correctly for the last element in a list
            start = bank.index(max(bank[start : end if end < 0 else None]), start)
            output.append(bank[start])
            end += 1
            start += 1
        return int("".join(str(n) for n in output))


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=3,
        test_answers=("357", "3121910778619"),
        test_input="""987654321111111
811111111111119
234234234234278
818181911112111""",
    )
    runner.cli()
