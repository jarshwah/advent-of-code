from collections import defaultdict
from functools import cmp_to_key

import utils


def in_order(update: tuple[int, ...], priorities: dict[int, list[int]]) -> bool:
    for order, pg in enumerate(update):
        if any(dep for dep in priorities[pg] if dep in update[order:]):
            return False
    return True


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Find update list that is already in order of priority and sum the middle value of each
        update.
        """
        rule_list, update_list = input.group().strings
        rules = [tuple(map(int, rule.split("|"))) for rule in rule_list]
        updates = [tuple(map(int, update.split(","))) for update in update_list]

        # Adjacency list is all numbers left of a given number in the priority list.
        priorities = defaultdict(list)
        for rule in rules:
            priorities[rule[1]].append(rule[0])

        result = 0
        for update in updates:
            if in_order(update, priorities):
                result += update[len(update) // 2]
        return result

    def part_two(self, input: utils.Input) -> str | int:
        """
        Find update list that is not in order of priority and sum the middle value of each update
        after sorting into order.
        """
        rule_list, update_list = input.group().strings
        rules = [tuple(map(int, rule.split("|"))) for rule in rule_list]
        updates = [tuple(map(int, update.split(","))) for update in update_list]
        priorities = defaultdict(list)
        for rule in rules:
            priorities[rule[1]].append(rule[0])

        def sorter(a: int, b: int) -> int:
            """An element comes first if it is not a dependency of the other."""
            return a if b in priorities[a] else -1

        result = 0
        key = cmp_to_key(sorter)
        for update in (update for update in updates if not in_order(update, priorities)):
            ordered = sorted(update, key=key)
            result += ordered[len(ordered) // 2]
        return result


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=5,
        test_answers=("143", "123"),
        test_input="""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""",
    )
    runner.cli()
