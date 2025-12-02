import math

import utils


class Puzzle(utils.Puzzle):
    """Find invalid product ids by looking for repeating sequences of numbers."""

    def part_one(self, input: utils.Input) -> str | int:
        """A repeating pattern exactly twice"""
        total_diff = 0
        for line in input.split(",").strings:
            start, end = list(map(int, line.split("-")[0:2]))
            total_diff += sum(
                self.repeating(product_id, min_length=math.ceil(len(str(product_id)) / 2))
                for product_id in range(start, end + 1)
            )
        return total_diff

    def part_two(self, input: utils.Input) -> str | int:
        """A repeating pattern at LEAST twice"""
        total_diff = 0
        for line in input.split(",").strings:
            start, end = list(map(int, line.split("-")[0:2]))
            total_diff += sum(
                self.repeating(product_id, min_length=1) for product_id in range(start, end + 1)
            )
        return total_diff

    def repeating(self, product_id: int, min_length: int) -> int:
        spid = str(product_id)
        length_spid = len(spid)
        for length in range(1, len(spid) // 2 + 1):
            if length < min_length:
                continue
            prefix = spid[:length]
            if all(
                (spid[start : start + length] == prefix for start in range(0, length_spid, length))
            ):
                return product_id
        return 0


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=2,
        test_answers=("1227775554", "4174379265"),
        test_input="""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""",
    )
    runner.cli()
