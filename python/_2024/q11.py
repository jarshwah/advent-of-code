from functools import cache

import utils


@cache
def mutate(stone: int, n: int) -> int:
    """
    Evolve a single stone N times.

    Cache the results to avoid recalculating the same stone multiple times.

    Stones evolve independently of one another, so results from one can feed the other.

    If we're at the final step, return 1, otherwise, follow the rules:
        1. If the stone is 0, return 1.
        2. If the stone has an even number of digits, split it in half, and evolve each half.
        3. Otherwise, multiply the stone by 2024.
    """
    if n == 0:
        return 1
    if stone == 0:
        return mutate(1, n - 1)
    if len(str(stone)) % 2 == 0:
        left, right = (
            int(str(stone)[: len(str(stone)) // 2]),
            int(str(stone)[len(str(stone)) // 2 :]),
        )
        return mutate(left, n - 1) + mutate((right), n - 1)
    return mutate(stone * 2024, n - 1)


class Puzzle(utils.Puzzle):
    """
    Given a list of numbers, mutate them according to the rules:
        - 0 -> 1
        - even num digits -> [left-half, right-half]
        - otherwise -> x*2024

    Then count the number of stones after N iterations.
    """

    def part_one(self, input: utils.Input) -> str | int:
        """
        Loop 25 times.

        The problem statement initially sounded like it'd be conways game of life, given
        the statement that each stone changes simultaneously, which is why maintaining
        a list of the actual values seemed important.

        Part 2 didn't expand on that direction though. The simultaneous bit is useless
        information, since each stone evolves independently in path parts.
        """
        stones = input.split().numbers
        for _ in range(25):
            new_stones = []
            for stone in stones:
                if stone == 0:
                    new_stones.append(1)
                elif len(str(stone)) % 2 == 0:
                    new_stones.extend(
                        [
                            int(str(stone)[: len(str(stone)) // 2]),
                            int(str(stone)[len(str(stone)) // 2 :]),
                        ]
                    )
                else:
                    new_stones.append(stone * 2024)
            stones = new_stones

        return len(stones)

    def part_one_alt(self, input: utils.Input) -> str | int:
        stones = input.split().numbers
        return sum(mutate(stone, 25) for stone in stones)

    def part_two(self, input: utils.Input) -> str | int:
        """
        Same, but loop 75 times.
        """
        stones = input.split().numbers
        return sum(mutate(stone, 75) for stone in stones)


puzzle = Puzzle(
    year=2024,
    day=11,
    test_answers=("55312", "65601038650482"),
    test_input="""125 17""",
)

if __name__ == "__main__":
    puzzle.cli()
