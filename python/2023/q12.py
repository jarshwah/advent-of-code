import ast
import re
from functools import lru_cache

import aocd

import utils

OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"


@lru_cache(maxsize=None)
def possible_configs(config: str, curr_matches: int, matches: tuple[int, ...]) -> int:
    if not config:
        # Exhausted our set
        if not curr_matches and not matches:
            # All matched, good
            return 1
        if len(matches) == 1 and curr_matches == matches[0]:
            # Last matched, good
            return 1
        # Didn't match
        return 0

    remaining_damaged = config.count(DAMAGED)
    remaining_unknown = config.count(UNKNOWN)
    remaining_matches = sum(matches)
    slots = remaining_damaged + remaining_unknown

    if curr_matches + slots < remaining_matches:
        # Not enough to match, exit early
        return 0

    if not matches and (curr_matches or remaining_damaged):
        # We have no matches left but remaining damaged, exit early
        return 0

    num_configs = 0
    check = config[0]

    if check == OPERATIONAL:
        if not curr_matches:
            # Continue on without any match
            num_configs += possible_configs(config[1:], 0, matches)
        elif curr_matches == matches[0]:
            # Completed the match
            num_configs += possible_configs(config[1:], 0, matches[1:])
        else:
            # We hit an operational mid-way through a match, exit early
            return 0

    elif check == UNKNOWN:
        if not curr_matches:
            # Branch into match and non-match
            num_configs += possible_configs(config[1:], 0, matches)
            num_configs += possible_configs(config[1:], 1, matches)
        elif curr_matches == matches[0]:
            # Match completed, continue to next match
            num_configs += possible_configs(config[1:], 0, matches[1:])
        else:
            # Continue matching the current
            num_configs += possible_configs(config[1:], curr_matches + 1, matches)

    elif check == DAMAGED:
        if not curr_matches:
            num_configs += possible_configs(config[1:], 1, matches)
        else:
            num_configs += possible_configs(config[1:], curr_matches + 1, matches)

    return num_configs


def matches(config: str, broken: tuple[int, ...]) -> int:
    check = f".{config}."  # pad with dots to make regex easier
    matcher = ""
    for digit in broken:
        matcher += rf"([\?\#]{{{digit}}})([\?\.]+)"

    matcher = r"(?=(\." + matcher + "))"
    # abort - not working.
    return len(re.findall(matcher, check))


def part_one(raw: str) -> int:
    reports = utils.Input(raw).lines().strings
    num_configurations = 0
    for report in reports:
        layout, broken = report.split()
        damaged_layout = ast.literal_eval(broken)
        num = possible_configs(layout, 0, damaged_layout)
        num_configurations += num
    return num_configurations


def part_two(raw: str) -> int:
    reports = utils.Input(raw).lines().strings
    num_configurations = 0
    for report in reports:
        layout, broken = report.split()
        expanded_layout = "?".join([layout] * 5)
        damaged_layout = ast.literal_eval(broken) * 5
        num = possible_configs(expanded_layout, 0, damaged_layout)
        num_configurations += num
    return num_configurations


def test():
    test_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 21, answer_1
    assert answer_2 == 525152, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=12, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
