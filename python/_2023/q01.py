import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        total = 0
        for line in input.lines().strings:
            nums = []
            for c in line:
                if c.isdigit():
                    nums.append(c)
            total += int(nums[0] + nums[-1])
        
        return total

    def part_two(self, input: utils.Input) -> str | int:
        words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
        total = 0
        for line in input.lines().strings:
            nums = []
            for idx, c in enumerate(line):
                if c.isdigit():
                    nums.append(c)
                else:
                    for num, word in enumerate(words, 1):
                        if line[idx : idx + len(word)].startswith(word):
                            nums.append(str(num))
                            break
            total += int(nums[0] + nums[-1])
        
        return total


puzzle = Puzzle(
    year=2023,
    day=1,
    test_answers=("142", "281"),
    test_input="""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""",
    test_input_2="""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""",
)

if __name__ == "__main__":
    puzzle.cli()