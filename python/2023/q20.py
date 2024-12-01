from __future__ import annotations

import dataclasses
import math
from collections import Counter, deque
from collections.abc import Sequence
from dataclasses import dataclass
from functools import reduce

import aocd

import utils


@dataclass(slots=True)
class Gate:
    name: str
    memory: Counter[bool] = dataclasses.field(default_factory=Counter)
    outputs: Sequence[str] = dataclasses.field(default_factory=list)

    def receive(self, input: Pulse) -> Sequence[Pulse]: ...

    def __eq__(self, other: Gate) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(slots=True)
class Pulse:
    from_gate: str
    to_gate: str
    signal: bool


@dataclass(slots=True)
class Button(Gate):
    name: str = "button"

    def receive(self, input: Pulse) -> Sequence[Pulse]:
        for gate in self.outputs:
            self.memory[input.signal] += 1
            yield Pulse(self.name, gate, input.signal)


@dataclass(slots=True)
class FlipFlop(Gate):
    current: int = False

    def receive(self, input: Pulse) -> Sequence[Pulse]:
        if input.signal:
            return

        self.current = not self.current
        for gate in self.outputs:
            self.memory[self.current] += 1
            yield Pulse(self.name, gate, self.current)


@dataclass(slots=True)
class Conjunction(Gate):
    current = False
    inputs: dict[str, bool] = dataclasses.field(default_factory=dict)

    def receive(self, input: Pulse) -> bool:
        self.inputs[input.from_gate] = input.signal
        signal_out = not all(self.inputs.values())
        for gate in self.outputs:
            self.memory[signal_out] += 1
            yield Pulse(self.name, gate, signal_out)

    def __eq__(self, other: Gate) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(slots=True)
class Broadcast(Gate):
    def receive(self, input: Pulse) -> Sequence[Pulse]:
        for gate in self.outputs:
            self.memory[input.signal] += 1
            yield Pulse(self.name, gate, input.signal)


@dataclass(slots=True)
class Output(Gate):
    name = "output"
    current: int = False

    def receive(self, input: Pulse) -> Sequence[Pulse]:
        self.current = not input.signal
        return []


def build_network(raw: str, output: str) -> dict[str, Gate]:
    network = {
        "button": Button("button", outputs=["broadcaster"]),
        output: Output(output),
    }
    conjunctions = set()
    for line in utils.Input(raw).lines().strings:
        left, right = line.split(" -> ")
        if left == "broadcaster":
            network["broadcaster"] = Broadcast("broadcaster", outputs=right.split(", "))
            continue
        sym, name = left[0], left[1:]
        outputs = right.split(", ")
        match sym:
            case "%":
                network[name] = FlipFlop(name, outputs=outputs)
            case "&":
                network[name] = Conjunction(name, outputs=outputs)
                conjunctions.add(name)
            case _:
                assert False
    for gate_name in network:
        for output_gate in network[gate_name].outputs:
            if output_gate in conjunctions:
                network[output_gate].inputs[gate_name] = False
    return network


def part_one(raw: str, output_gate: str) -> int:
    network = build_network(raw, output_gate)
    for button_push in range(1000):
        queue = deque([Pulse("button", "button", False)])
        while queue:
            pulse = queue.popleft()
            gate = network[pulse.to_gate]
            for output in gate.receive(pulse):
                queue.append(output)
    memory = reduce(lambda a, b: a + b, (gate.memory for gate in network.values()))
    return memory[True] * memory[False]


def part_two(raw: str, output_gate: str) -> int:
    network = build_network(raw, output_gate)
    rx_parent = utils.only(
        network[gate] for gate in network if output_gate in network[gate].outputs
    )
    if not isinstance(rx_parent, Conjunction):
        raise ValueError("rx parent is not a conjunction")

    parents = {
        parent_gate.name: 0
        for gate in rx_parent.inputs
        if (parent_gate := network[gate]) and isinstance(parent_gate, Conjunction)
    }

    # We need RX to deliver a LOW pulse, which means
    #   -> all of its parents have delivered a HIGH pulse.
    # All of the parents must deliver a HIGH pulse, which means
    #   -> that any of the inputs were LOW.

    button_push = 0
    while True:
        button_push += 1
        queue = deque([Pulse("button", "button", False)])
        while queue:
            pulse = queue.popleft()
            # Checking at the end of the button push does not work, we need to detect
            # the cycle mid-push (and lucky that it's an immediate cycle from the beginning of the period)
            if not pulse.signal and pulse.to_gate in parents and parents[pulse.to_gate] == 0:
                parents[pulse.to_gate] = button_push
            gate = network[pulse.to_gate]
            for output in gate.receive(pulse):
                queue.append(output)

        if all(parents.values()):
            return math.lcm(*parents.values())


def test():
    test_input = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    answer_1 = part_one(test_input, output_gate="output")
    assert answer_1 == 11687500, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=20, year=2023)
    print("Part 1: ", part_one(data, output_gate="rx"))
    print("Part 2: ", part_two(data, output_gate="rx"))
