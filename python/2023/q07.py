from collections import Counter
from dataclasses import dataclass

import aocd

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
        return max(
            (
                self.best_hand(tuple(wild if card == 1 else card for card in cards))
                for wild in NON_WILDS
            )
        ), *cards


def get_hands(raw: str) -> list[Hand]:
    hands = []
    for line in utils.Input(raw).lines().strings:
        cards = tuple(CARDS[card] for card in line.split()[0])
        assert len(cards) == 5
        bid = int(line.split()[1])
        hands.append(Hand(cards, bid))
    return hands


def part_one(hands: list[Hand]) -> int:
    hands.sort(key=lambda hand: hand.result())
    return sum(hand.bid * rank for rank, hand in enumerate(hands, 1))


def part_two(hands: list[Hand]) -> int:
    hands.sort(key=lambda hand: hand.result_wilds())
    return sum(hand.bid * rank for rank, hand in enumerate(hands, 1))


def test():
    test_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    hands = get_hands(test_input)
    answer_1 = part_one(hands)
    answer_2 = part_two(hands)
    assert answer_1 == 6440, answer_1
    assert answer_2 == 5905, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=7, year=2023)
    hands = get_hands(data)
    print("Part 1: ", part_one(hands))
    print("Part 2: ", part_two(hands))
