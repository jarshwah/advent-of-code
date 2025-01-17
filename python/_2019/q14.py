import math
from collections import defaultdict

import utils

type Chem = str
type Amount = int
type Reactions = dict[Chem, tuple[int, list[tuple[int, Chem]]]]


class Puzzle(utils.Puzzle):
    """--- Day 14: Space Stoichiometry ---"""

    def get_reactions(self, input: utils.Input) -> Reactions:
        reactions: Reactions = {}
        for react in input.lines().strings:
            inputs, output = react.split(" => ")
            output_num, output_chem = output.split(" ")
            deps = []
            for input_react in inputs.split(", "):
                input_num, input_chem = input_react.split(" ")
                deps.append((int(input_num), input_chem))
            reactions[output_chem] = (int(output_num), deps)
        return reactions

    def ore_required(
        self, reactions: Reactions, chemical: str, num: int, leftover: defaultdict[str, int]
    ) -> int:
        if chemical == "ORE":
            return num

        if num <= leftover[chemical]:
            leftover[chemical] -= num
            return 0

        num -= leftover[chemical]
        leftover[chemical] = 0
        ore = 0
        produce_quantity, inputs = reactions[chemical]
        multiple = math.ceil(num / produce_quantity)
        for in_req, in_chem in inputs:
            in_req *= multiple
            ore += self.ore_required(reactions, in_chem, in_req, leftover)
        leftover[chemical] += multiple * produce_quantity - num
        return ore

    def both_parts(self, input: utils.Input) -> tuple[int | str, int | str]:
        reactions = self.get_reactions(input)
        ore_1_fuel = self.ore_required(reactions, "FUEL", 1, defaultdict(int))
        stocked = 1000000000000
        low = stocked // ore_1_fuel
        high = low + (low // 2)
        max_fuel = utils.binary_search(
            low,
            high,
            lambda check: self.ore_required(reactions, "FUEL", check, defaultdict(int)) <= stocked,
        )

        return ore_1_fuel, max_fuel


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=14,
        both=True,
        test_answers=("13312", "82892753"),
        test_input="""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""",
    )
    runner.cli()
