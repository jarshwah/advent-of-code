import utils

type Ranges = list[tuple[int, int]]


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        range_strs, ingredients_str = input.group("\n\n", "\n").strings
        ingredients = list(map(int, ingredients_str))
        ranges: Ranges = [tuple(map(int, range_str.split("-"))) for range_str in range_strs]  # type: ignore [misc]
        ranges = compress_ranges(ranges)
        fresh = 0
        for ingredient in ingredients:
            for check in ranges:
                if check[0] <= ingredient <= check[1]:
                    fresh += 1
                    break
        return fresh

    def part_two(self, input: utils.Input) -> str | int:
        range_strs, _ = input.group("\n\n", "\n").strings
        ranges: Ranges = [tuple(map(int, range_str.split("-"))) for range_str in range_strs]  # type: ignore [misc]
        ranges = compress_ranges(ranges)
        return sum(end - start + 1 for start, end in ranges)


def compress_ranges(ranges: Ranges) -> Ranges:
    ranges.sort()
    new_ranges: Ranges = []
    start, end = ranges[0]
    for rng in ranges[1:]:
        if rng[0] <= end:
            # we're inside the current range, compress
            end = max(rng[1], end)
            continue
        # we're outside the current range, start a new one.
        new_ranges.append((start, end))
        start, end = rng
    new_ranges.append((start, end))
    return new_ranges


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=5,
        test_answers=("3", "14"),
        test_input="""3-5
10-14
16-20
12-18

1
5
8
11
17
32""",
    )
    runner.cli()
