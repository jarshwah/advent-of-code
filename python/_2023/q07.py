from collections import Counter
from dataclasses import dataclass

import utils

CARDS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

NON_WILDS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14)


@dataclass(order=True)
class Hand:
    cards: tuple[int, int, int, int, int]
    bid: int

    def best_hand(self, cards: tuple[int, int, int, int, int]) -> int:
        counts = tuple(sorted(Counter(cards).values()))
        match counts:
            case (1, 1, 1, 1, 1):  # high card
                return 100
            case (1, 1, 1, 2):  # 1 pair
                return 200
            case (1, 2, 2):  # 2 pair
                return 300
            case (1, 1, 3):  # 3 of a kind
                return 400
            case (2, 3):  # full house
                return 500
            case (1, 4):  # 4 of a kind
                return 600
            case (5,):  # 5 of a kind
                return 700
            case _:
                raise ValueError

    def result(self) -> tuple[int, int, int, int, int, int]:
        return self.best_hand(self.cards), *self.cards

    def result_wilds(self) -> tuple[int, int, int, int, int, int]:
        # Jacks are Jokers (wild), they are worth 1 point individually, but can
        # be used as any other card to make the best hand.
        cards = tuple(1 if card == 11 else card for card in self.cards)
        if 1 not in cards:
            return self.result()

        # Find the best hand by replacing the wilds with the most common card
        no_wilds = tuple(card for card in cards if card != 1)
        top = 14 if not no_wilds else Counter(no_wilds).most_common()[0][0]
        replacement_cards = tuple(top if card == 1 else card for card in cards)
        return self.best_hand(replacement_cards), *cards


def get_hands(raw: str) -> list[Hand]:
    hands = []
    for line in utils.Input(raw).lines().strings:
        cards = tuple(CARDS[card] for card in line.split()[0])
        assert len(cards) == 5
        bid = int(line.split()[1])
        hands.append(Hand(cards, bid))
    return hands


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        hands = get_hands(input.string)
        hands.sort(key=lambda hand: hand.result())
        return sum(hand.bid * rank for rank, hand in enumerate(hands, 1))

    def part_two(self, input: utils.Input) -> str | int:
        hands = get_hands(input.string)
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
