from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field

import utils


@dataclass
class Monkey:
    number: int
    items: list[int] = field(default_factory=list)
    operation: Callable[[int], int] = lambda old: old
    test_divisor: int = 1
    true_target: int = 0
    false_target: int = 0
    inspections: int = 0

    def exec_turn(self, reducer: Callable[[int], int], monkeys: list[Monkey]) -> None:
        for item in self.items:
            self.inspections += 1
            item = self.operation(item)
            item = reducer(item)
            if item % self.test_divisor == 0:
                monkeys[self.true_target].items.append(item)
            else:
                monkeys[self.false_target].items.append(item)
        self.items.clear()


def parse(raw: str) -> list[Monkey]:
    groups = raw.strip().split("\n\n")
    monkeys = []
    for gp in groups:
        monkey = Monkey(number=len(monkeys))
        for line in gp.split("\n"):
            line = line.strip()
            if line.startswith("Starting items:"):
                monkey.items = [int(num) for num in line.split(": ")[1].split(", ")]
            elif line.startswith("Operation:"):
                exec(f"monkey.operation = lambda old: {line.split(' = ')[1]}")
            elif line.startswith("Test:"):
                monkey.test_divisor = int(line.split()[-1])
            elif line.startswith("If true:"):
                monkey.true_target = int(line.split()[-1])
            elif line.startswith("If false:"):
                monkey.false_target = int(line.split()[-1])
        monkeys.append(monkey)
    return monkeys


def solve(monkeys: list[Monkey], rounds: int, reducer: Callable[[int], int]) -> int:
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.exec_turn(reducer, monkeys)
    inspection_counts = sorted([m.inspections for m in monkeys], reverse=True)
    return inspection_counts[0] * inspection_counts[1]


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        monkeys = parse(input.string)

        def reducer(item: int) -> int:
            return item // 3

        return solve(monkeys, 20, reducer)

    def part_two(self, input: utils.Input) -> str | int:
        monkeys = parse(input.string)
        reduction = math.lcm(*[m.test_divisor for m in monkeys])

        def reducer(item: int) -> int:
            return item % reduction

        return solve(monkeys, 10000, reducer)


puzzle = Puzzle(
    year=2022,
    day=11,
    test_answers=("10605", "2713310158"),
    test_input="""Monkey 0:
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
    If false: throw to monkey 1""",
)

if __name__ == "__main__":
    puzzle.cli()
