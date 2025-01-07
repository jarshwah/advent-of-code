import utils


def fuel_required(mass: int) -> int:
    return mass // 3 - 2


class Puzzle(utils.Puzzle):
    """--- Day 1: The Tyranny of the Rocket Equation ---"""

    def part_one(self, input: utils.Input) -> str | int:
        """
        How much fuel does each module require?
        """
        return sum(fuel_required(mass) for mass in input.lines().integers)

    def part_two(self, input: utils.Input) -> str | int:
        """
        Fuel also adds mass and therefore requires more fuel.
        """
        fuel = 0
        for mass in input.lines().integers:
            while (mass := fuel_required(mass)) > 0:
                fuel += mass
        return fuel


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=1,
        test_answers=("33583", "50346"),
        test_input="""100756""",
    )
    runner.cli()
