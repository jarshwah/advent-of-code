from collections import defaultdict
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        data = input.lines().strings
        # line = Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        total = 0
        for line in data:
            winning_str, ours_str = line.split(":")[1].split("|")
            winning = {int(num) for num in winning_str.split()}
            ours = {int(num) for num in ours_str.split()}
            matched = winning & ours
            if matched:
                total += 2 ** (len(matched) - 1)
        return total

    def part_two(self, input: utils.Input) -> str | int:
        data = input.lines().strings
        # line = Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        counter = defaultdict(lambda: 1)
        total = 0
        for line in data:
            card_str, game_str = line.split(":")
            card_num = int(card_str.split()[1])
            winning_str, ours_str = game_str.split("|")
            winning = {int(num) for num in winning_str.split()}
            ours = {int(num) for num in ours_str.split()}
            matched = winning & ours
            for num, _ in enumerate(matched, start=card_num + 1):
                counter[num] += counter[card_num]
            total += counter[card_num]
        return total


puzzle = Puzzle(
    year=2023,
    day=4,
    test_answers=("13", "30"),
    test_input="""\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""",
)

if __name__ == "__main__":
    puzzle.cli()
