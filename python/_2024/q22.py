from collections import Counter, deque

import utils

type PriceChange = tuple[int, ...]


def next(n: int) -> int:
    n = ((n * 64) ^ n) % 16777216
    n = ((n // 32) ^ n) % 16777216
    n = ((n * 2048) ^ n) % 16777216
    return n


class Puzzle(utils.Puzzle):
    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        """
        Generate a psuedo-random sequence of 2000 numbers for each money.

        Part 1: sum the 2000th number for each monkey.
        Part 2: find the best sequence of 4 price changes that end on the highest last digit.
        """
        sequences: Counter[PriceChange] = Counter()
        secrets = 0
        for monkey in input.lines().numbers:
            # Unroll the first 4 iterations to get the initial sequence
            m1 = next(monkey)
            m2 = next(m1)
            m3 = next(m2)
            m4 = next(m3)
            seq = deque(
                [m1 % 10 - monkey % 10, m2 % 10 - m1 % 10, m3 % 10 - m2 % 10, m4 % 10 - m3 % 10],
                maxlen=4,
            )
            seen: dict[PriceChange, int] = {tuple(seq): m4 % 10}
            monkey = m4
            for _ in range(2000 - 4):
                next_monkey = next(monkey)
                next_price = next_monkey % 10
                seq.append(next_price - monkey % 10)
                key = tuple(seq)
                if key not in seen:
                    # Only store the first time we see a sequence for each monkey
                    seen[key] = next_price
                monkey = next_monkey
            for key, value in seen.items():
                sequences[key] += value
            secrets += monkey
        return secrets, sequences.most_common(1)[0][1]


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=22,
        both=True,
        test_answers=("37990510", "23"),
        test_input="""1
2
3
2024""",
    )
    runner.cli()
