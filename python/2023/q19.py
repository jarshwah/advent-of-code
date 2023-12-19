import math
import operator
from collections import deque

import aocd
from parse import parse

import utils

parts_template = "{{x={xnum:d},m={mnum:d},a={anum:d},s={snum:d}}}"
wf_rule_template = "{xmas}{op}{compare:d}:{wf_name}"
OPERATORS = {
    ">": operator.gt,
    "<": operator.lt,
}


def part_one(raw: str) -> int:
    workflow_list, part_lists = utils.Input(raw).group("\n\n", "\n").strings
    accepted_part_lists = []
    rejected_part_lists = []
    parts = []
    for part_list in part_lists:
        X, M, A, S = parse(parts_template, part_list).named.values()
        parts.append({"x": X, "m": M, "a": A, "s": S})

    workflows = {}
    for wf in workflow_list:
        wf_name, wf_rule_list = wf.split("{")
        *wf_rules, wf_end = wf_rule_list[:-1].split(",")
        wf_parts = [parse(wf_rule_template, part).named for part in wf_rules]
        workflows[wf_name] = (wf_parts, wf_end)

    for part in parts:
        current_workflow = "in"
        while current_workflow not in ("A", "R"):
            rules, end_state = workflows[current_workflow]
            for rule in rules:
                xmas, op, compare, new_workflow = rule.values()
                left = part[xmas]
                if OPERATORS[op](left, compare):
                    current_workflow = new_workflow
                    break
            else:
                current_workflow = end_state

        if current_workflow == "R":
            rejected_part_lists.append(part)

        if current_workflow == "A":
            accepted_part_lists.append(part)
            continue

    return sum(sum(part.values()) for part in accepted_part_lists)


def part_two(raw: str) -> int:
    # return part_two_alt(raw)
    workflow_list, _ = utils.Input(raw).group("\n\n", "\n").strings
    workflows = {}
    for wf in workflow_list:
        wf_name, wf_rule_list = wf.split("{")
        *wf_rules, wf_end = wf_rule_list[:-1].split(",")
        wf_parts = [parse(wf_rule_template, part).named for part in wf_rules]
        workflows[wf_name] = (wf_parts, wf_end)

    combinations = 0
    part_list = [(1, 4000), (1, 4000), (1, 4000), (1, 4000)]
    queue = deque([(part_list, "in")])
    while queue:
        parts, current_workflow = queue.pop()
        if current_workflow == "R":
            continue
        if current_workflow == "A":
            combinations += math.prod(hi - lo + 1 for lo, hi in parts)
            continue

        rules, last_workflow = workflows[current_workflow]
        for rule in rules:
            xmas, op, compare, new_workflow = rule.values()
            part_num = "xmas".index(xmas)
            lower, high = parts[part_num]
            match op:
                case ">":
                    if lower > compare:
                        # The range is fully inside, proceed to next workflow
                        #   eg: (1000, 2000) > 999:
                        #       -> (1000, 2000) into next workflow
                        queue.append((parts, new_workflow))
                        break

                    if high <= compare:
                        # The range is fully outside, continue to next rule as-is
                        #   eg: (1000, 2000) > 2000:
                        #        -> (1000, 2000) into next rule
                        continue

                    # The range is partially inside, so we need to split it
                    # (1000, 2000) > 1500
                    #       next -> (1501, 2000)
                    #   continue -> (1000, 1500)

                    # Continue on by shrinking our lower bound to fit
                    next_parts = parts[::]
                    next_parts[part_num] = (compare + 1, high)
                    queue.append((next_parts, new_workflow))

                    # And continue by shrinking our upper bound to fit
                    parts[part_num] = (lower, compare)
                case "<":
                    if compare <= lower:
                        # Fully outside
                        continue

                    if compare >= high:
                        # Fully inside
                        queue.append((parts, new_workflow))
                        break

                    # Partially inside
                    # (500, 1000) < 800 (middle)
                    #        next -> (500, 799)
                    #    continue -> (800, 1000)
                    next_parts = parts[::]
                    next_parts[part_num] = (lower, compare - 1)
                    queue.append((next_parts, new_workflow))

                    # And continue by shrinking our lower bound to fit
                    parts[part_num] = (compare, high)
        queue.append((parts, last_workflow))
    return combinations


def part_two_alt(raw: str) -> int:
    workflow_list, _ = utils.Input(raw).group("\n\n", "\n").strings
    workflows = {}
    for wf in workflow_list:
        wf_name, wf_rule_list = wf.split("{")
        *wf_rules, wf_end = wf_rule_list[:-1].split(",")
        wf_parts = [parse(wf_rule_template, part).named for part in wf_rules]
        workflows[wf_name] = wf_parts, wf_end

    parts = {
        "x": range(1, 4001),
        "m": range(1, 4001),
        "a": range(1, 4001),
        "s": range(1, 4001),
    }
    return combos(parts, "in", workflows)


def combos(parts: dict[str, range], current_workflow: str, workflows: dict) -> int:
    if current_workflow == "R":
        return 0
    if current_workflow == "A":
        return math.prod(rg.stop - rg.start for rg in parts.values())

    combinations = 0
    our_parts = parts.copy()
    rules, last_workflow = workflows[current_workflow]
    for rule in rules:
        xmas, op, compare, new_workflow = rule.values()
        match op:
            case ">":
                matched = range(compare + 1, our_parts[xmas].stop)
                continue_with = range(our_parts[xmas].start, compare + 1)
            case "<":
                matched = range(our_parts[xmas].start, compare)
                continue_with = range(compare, our_parts[xmas].stop)

        our_parts[xmas] = matched
        combinations += combos(our_parts, new_workflow, workflows)
        our_parts[xmas] = continue_with
    combinations += combos(our_parts, last_workflow, workflows)
    return combinations


def test():
    test_input = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 19114, answer_1
    assert answer_2 == 167409079868000, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=19, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
