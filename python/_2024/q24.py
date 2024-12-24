from dataclasses import dataclass
from graphlib import TopologicalSorter

from parse import parse

import utils


@dataclass
class Wire:
    name: str
    output: bool | None
    inputs: tuple[str, str]
    gate_type: str


def get_bits(wires: dict[str, Wire], prefix: str) -> str:
    return "".join(
        str(int(w.output))
        for w in sorted(wires.values(), key=lambda w: w.name)
        if w.name.startswith(prefix) and w.output is not None
    )


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        init, gates = input.group(sep="\n").strings
        topo: TopologicalSorter[str] = TopologicalSorter()
        wires = {}
        for gate_str in gates:
            gate = parse("{left} {gate_type} {right} -> {output}", gate_str)
            topo.add(gate["output"], gate["left"], gate["right"])
            wires[gate["output"]] = Wire(
                name=gate["output"],
                output=None,
                inputs=(gate["left"], gate["right"]),
                gate_type=gate["gate_type"],
            )
        for i in init:
            wname, val = i.split(": ")
            wires[wname] = Wire(
                name=wname, output=bool(int(val)), inputs=("", ""), gate_type="identity"
            )
        dependencies = list(topo.static_order())
        simulate(wires, dependencies)
        bits = get_bits(wires, "z")[::-1]
        return int(bits, 2)

    def part_two(self, input: utils.Input) -> str | int:
        if self.testing:
            return "no-answer"
        _, gates = input.group(sep="\n").strings
        wires: dict[str, Wire] = {}
        for gate_str in gates:
            gate = parse("{left} {gate_type} {right} -> {output}", gate_str)
            wires[gate["output"]] = Wire(
                name=gate["output"],
                output=None,
                inputs=(gate["left"], gate["right"]),
                gate_type=gate["gate_type"],
            )

        bad_wires = set()
        for wire in wires.values():
            if wire.name in ("z00", "z45"):
                # Skip the first and last Z gates as they aren't standard.
                continue

            if "x00" in wire.inputs or "y00" in wire.inputs:
                # Skip the first inputs as they are not standard.
                continue

            # All outputs are XOR gates
            if wire.name.startswith("z") and wire.gate_type != "XOR":
                bad_wires.add(wire.name)
                continue

            # All XOR gates either output to Z or input from X or Y
            if (
                wire.gate_type == "XOR"
                and not wire.name.startswith("z")
                and not wire.inputs[0].startswith(("x", "y"))
                and not wire.inputs[1].startswith(("x", "y"))
            ):
                bad_wires.add(wire.name)
                continue

            # No XOR gate ever outputs to an OR gate
            if wire.gate_type == "XOR":
                for target in wires.values():
                    if wire.name in target.inputs and target.gate_type == "OR":
                        bad_wires.add(wire.name)
                        break

            # All AND gates output to an OR gate
            if wire.gate_type == "AND":
                for target in wires.values():
                    if wire.name in target.inputs and target.gate_type != "OR":
                        bad_wires.add(wire.name)
                        break

        bad_wire_report = ",".join(sorted(bad_wires))
        return bad_wire_report


def simulate(wires: dict[str, Wire], dependencies: list[str]) -> None:
    for wire_name in dependencies:
        wire = wires[wire_name]
        if wire.inputs == ("", ""):
            continue
        left = wires[wire.inputs[0]]
        right = wires[wire.inputs[1]]
        if left.output is None or right.output is None:
            raise ValueError("Not all inputs are known")
        if wire.gate_type == "AND":
            wire.output = left.output & right.output
        elif wire.gate_type == "OR":
            wire.output = left.output | right.output
        elif wire.gate_type == "XOR":
            wire.output = left.output ^ right.output
        elif wire.gate_type == "identity":
            wire.output = left.output
        else:
            raise ValueError(f"Unknown gate type: {wire.gate_type}")


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=24,
        test_answers=("2024", "no-answer"),
        test_input="""x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj""",
    )
    runner.cli()
