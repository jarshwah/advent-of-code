from collections import Counter
from dataclasses import dataclass
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        hands.sort(key=lambda hand: hand.result())
        return sum(hand.bid * rank for rank, hand in enumerate(hands, 1))

    def part_two(self, input: utils.Input) -> str | int:
        hands.sort(key=lambda hand: hand.result_wilds())
        return sum(hand.bid * rank for rank, hand in enumerate(hands, 1))


puzzle = Puzzle(
    year=2023,
    day=7,
    test_answers=("6440", "5905"),
    test_input="""\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""",
)

if __name__ == "__main__":
    puzzle.cli()
