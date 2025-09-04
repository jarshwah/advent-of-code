import itertools
from collections.abc import Iterable

import utils

type Signal = list[int]


def pattern(dx: int) -> Iterable[int]:
    assert dx > 0
    base_pattern = (0, 1, 0, -1)
    # keep cycling through the pattern
    pat = itertools.cycle(
        # chain the repetitions together
        itertools.chain(
            # repeat each digit by the 1-position of the output being calculated
            *[itertools.repeat(bp, dx) for bp in base_pattern]
        )
    )
    next(pat)  # skip the very first value
    return pat


def fft(signal: Signal) -> Signal:
    out = []
    for dx in range(1, len(signal) + 1):
        out.append(abs(sum(lh * rh for lh, rh in zip(signal, pattern(dx)))) % 10)
    return out


class Puzzle(utils.Puzzle):
    """--- Day 16: Flawed Frequency Transmission ---"""

    def part_one(self, input: utils.Input) -> str | int:
        in_signal = list(map(int, list(input.string)))
        for _ in range(100):
            in_signal = fft(in_signal)
        return "".join(str(ix) for ix in in_signal[:8])

    def part_two(self, input: utils.Input) -> str | int:
        in_signal = list(map(int, list(input.string))) * 10_000
        offset = int("".join(str(i) for i in in_signal[:7]))
        in_signal = in_signal[:offset]
        for _ in range(100):
            in_signal = fft(in_signal)
        return "".join(str(ix) for ix in in_signal[offset : offset + 8])


puzzle = Puzzle(
    year=2019,
    day=16,
    test_answers=("24176176", ""),
    test_input="""80871224585914546619083218645595""",
)

if __name__ == "__main__":
    puzzle.cli()
