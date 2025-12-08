import math
from itertools import combinations

import utils


class Puzzle(utils.Puzzle):
    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        p1 = p2 = 0
        circuits = {tuple(nums[:3]): {tuple(nums[:3])} for nums in input.lines().split(",").numbers}
        pairs = sorted(combinations(circuits, 2), key=lambda pair: math.dist(*pair))
        lines = 10 if self.testing else 1000
        for idx, (j1, j2) in enumerate(pairs, 1):
            # Find the circuits the junctions are currently attached to
            c1 = utils.first((circuit for circuit in circuits if j1 in circuits[circuit]))
            c2 = utils.first((circuit for circuit in circuits if j2 in circuits[circuit]))
            if c1 != c2:
                # If not already connected, merge the circuits
                circuits[c1] |= circuits[c2]
                circuits.pop(c2)
            if idx == lines:
                # Multiply the length of the 3 largest circuits after N attempts
                p1 = math.prod(sorted((len(circuits[j]) for j in circuits), reverse=True)[:3])
            if len(circuits) == 1:
                # Multiply the X-coords of the last junctions to be connected
                p2 = j1[0] * j2[0]
                break
        return p1, p2


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=8,
        both=True,
        test_answers=("40", "25272"),
        test_input="""162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""",
    )
    runner.cli()
