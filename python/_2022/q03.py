import string
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        total = 0
        for rucksack in input.split().strings:
            left, right = utils.partition_middle(rucksack)
            common = utils.only(set(left).intersection(set(right)))
            total += priority.index(common)
        return total

    def part_two(self, input: utils.Input) -> str | int:
        total = 0
        rucksacks = input.split().strings
        for sacks in utils.chunked(rucksacks, 3):
            common = utils.only(set.intersection(*[set(sack) for sack in sacks]))
            total += priority.index(common)
        return total


puzzle = Puzzle(
    year=2022,
    day=3,
    test_answers=("157", "70"),
    test_input="""\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""",
)

if __name__ == "__main__":
    puzzle.cli()
