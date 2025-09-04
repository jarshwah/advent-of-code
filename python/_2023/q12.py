import ast
from functools import cache
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        reports = input.lines().strings
        num_configurations = 0
        for report in reports:
            layout, broken = report.split()
            damaged_layout = ast.literal_eval(broken)
            num = possible_configs(layout, 0, damaged_layout)
            num_configurations += num
        return num_configurations

    def part_two(self, input: utils.Input) -> str | int:
        reports = input.lines().strings
        num_configurations = 0
        for report in reports:
            layout, broken = report.split()
            expanded_layout = "?".join([layout] * 5)
            damaged_layout = ast.literal_eval(broken) * 5
            num = possible_configs(expanded_layout, 0, damaged_layout)
            num_configurations += num
        return num_configurations


puzzle = Puzzle(
    year=2023,
    day=12,
    test_answers=("21", "525152"),
    test_input="""\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""",
)

if __name__ == "__main__":
    puzzle.cli()
