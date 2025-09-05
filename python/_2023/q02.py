import re
from collections import Counter, defaultdict
from math import prod

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        data = input.lines().strings
        valid = 0
        for line in data:
            game_number = int(line.split(":")[0].split()[1])
            impossible = False
            for sets in line.split(":")[1].split(";"):
                start = Counter({"red": 12, "green": 13, "blue": 14})
                compare = Counter(
                    {match[1]: int(match[0]) for match in re.findall(r"(\d+) (\w+)", sets)}
                )
                if len(start - compare) < 3:
                    impossible = True
                    break
            if not impossible:
                valid += game_number
        return valid

    def part_two(self, input: utils.Input) -> str | int:
        data = input.lines().strings
        total = 0
        for line in data:
            counts = defaultdict(list)
            for match in re.findall(r"(\d+) (\w+)", line):
                counts[match[1]].append(int(match[0]))
            total += prod([max(nums) for nums in counts.values()])
        return total


puzzle = Puzzle(
    year=2023,
    day=2,
    test_answers=("8", "2286"),
    test_input="""\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""",
)

if __name__ == "__main__":
    puzzle.cli()
