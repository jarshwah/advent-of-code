import utils


class Puzzle(utils.Puzzle):
    """--- Day 6: Universal Orbit Map ---"""

    def part_one(self, input: utils.Input) -> str | int:
        """Find the number of direct and indirect orbits"""
        orbits = {}
        for orbitting, orbitter in input.group("\n", ")").strings:
            orbits[orbitter] = orbitting
        num_orbits = 0
        for orbitter in orbits.keys():
            num_orbits += 1
            orbitting = orbits[orbitter]
            while orbitting != "COM":
                num_orbits += 1
                orbitting = orbits[orbitting]

        return num_orbits

    def part_two(self, input: utils.Input) -> str | int:
        """Find the number of steps between SAN and YOU not including direct orbits of either"""
        orbits = {}
        for orbitting, orbitter in input.group("\n", ")").strings:
            orbits[orbitter] = orbitting
        san_orbitting, you_orbitting = orbits["SAN"], orbits["YOU"]
        san_visits, you_visits = {san_orbitting: 0}, {you_orbitting: 0}
        # find the common ancestor, and count steps
        # generate a path to com for each, then find the minimum count ancestor
        for orbitting, visitor, count in [
            (san_orbitting, san_visits, 0),
            (you_orbitting, you_visits, 0),
        ]:
            # TODO (optimisation): generate a single path to com, then the second can
            # stop as soon as there is a match
            while orbitting != "COM":
                orbitting = orbits[orbitting]
                count += 1
                visitor[orbitting] = count
        common = set(san_visits.keys()) & set(you_visits.keys())
        min_san = min(san_visits[key] for key in common)
        min_you = min(you_visits[key] for key in common)
        return min_san + min_you


puzzle = Puzzle(
    year=2019,
    day=6,
    test_answers=("54", "4"),
    test_input="""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""",
)

if __name__ == "__main__":
    puzzle.cli()
