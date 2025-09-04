from __future__ import annotations
import dataclasses
import math
from collections import Counter, deque
from collections.abc import Sequence
from dataclasses import dataclass
from functools import reduce
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
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

    def part_two(self, input: utils.Input) -> str | int:
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


puzzle = Puzzle(
    year=2023,
    day=20,
    test_answers=("", ""),
    test_input="""\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""",
)

if __name__ == "__main__":
    puzzle.cli()
