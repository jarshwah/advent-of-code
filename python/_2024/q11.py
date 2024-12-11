from functools import cache

import utils


@cache
def mutate(stone: int, n: int) -> int:
    if n == 0:
        return 1
    if stone == 0:
        return mutate(1, n - 1)
    if len(str(stone)) % 2 == 0:
        return mutate(int(str(stone)[: len(str(stone)) // 2]), n - 1) + mutate(
            int(str(stone)[len(str(stone)) // 2 :]), n - 1
        )

    return mutate(stone * 2024, n - 1)


class Puzzle(utils.Puzzle):
    """
    Given a list of numbers, mutate them according to the rules:
        - 0 -> 1
        - even num digits -> [left-half, right-half]
        - otherwise -> x*2024

    Then sum the number of stones after N iterations.
    """

    def part_one(self, input: utils.Input) -> str | int:
        """
        Loop 25 times
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


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=11,
        test_answers=("55312", "65601038650482"),
        test_input="""125 17""",
    )
    runner.cli()
