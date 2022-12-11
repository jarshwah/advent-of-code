from __future__ import annotations

import copy
import math
import operator
import typing as t
from collections import deque
from dataclasses import dataclass

import aocd
import utils


@dataclass
class Monkey:
    operator: t.Callable[[int, int], int]
    operand: int
    test_divisor: int
    if_true: int
    if_false: int
    items: deque[int]
    inspected: int = 0

    def inspect_item(self, reducer: t.Callable[[int], int]) -> tuple[int, int]:
        self.inspected += 1
        item = self.items.popleft()
        new_worry = reducer(self.operator(item, self.operand))
        return (
            (self.if_true, new_worry)
            if (new_worry % self.test_divisor) == 0
            else (self.if_false, new_worry)
        )


def parse(raw: str) -> list[Monkey]:
    data = utils.Input(raw).group("\n\n", "\n").strings
    monkeys = []
    for monkey in data:
        items = [int(item.strip()) for item in monkey[1].split(":")[1].split(",")]
        op, operand = monkey[2].split("old ")[1].split()
        oper = operator.mul if op == "*" else operator.add
        if operand == "old":
            operand = "2"
            oper = operator.pow
        divisor = int(monkey[3].split("divisible by ")[1])
        if_true = int(monkey[4][-1])
        if_false = int(monkey[5][-1])
        monkeys.append(
            Monkey(
                operator=oper,
                operand=int(operand),
                test_divisor=divisor,
                if_true=if_true,
                if_false=if_false,
                items=deque(items),
            )
        )
    return monkeys


def solve(monkeys: list[Monkey], rounds: int, reducer: t.Callable[[int, int], int]) -> int:
    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                new_monkey, new_worry = monkey.inspect_item(reducer)
                monkeys[new_monkey].items.append(new_worry)
    inspections = sorted([m.inspected for m in monkeys], reverse=True)
    return math.prod(inspections[:2])


def part_one(monkeys: list[Monkey]) -> int:
    def reducer(item: int) -> int:
        return item // 3

    return solve(monkeys, 20, reducer)


def part_two(monkeys: list[Monkey]) -> int:
    reduction = math.lcm(*[m.test_divisor for m in monkeys])

    def reducer(item: int) -> int:
        return item % reduction

    return solve(monkeys, 10000, reducer)


def test():
    test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
    monkeys = parse(test_input)
    monkeys_2 = copy.deepcopy(monkeys)
    answer_1 = part_one(monkeys)
    answer_2 = part_two(monkeys_2)
    assert answer_1 == 10605, answer_1
    assert answer_2 == 2713310158, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=11, year=2022)
    monkeys = parse(data)
    monkeys_2 = copy.deepcopy(monkeys)
    print("Part 1: ", part_one(monkeys))
    print("Part 2: ", part_two(monkeys_2))
