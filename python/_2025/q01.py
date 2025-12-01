import utils


class Puzzle(utils.Puzzle):
    """
    Unlock the safe. The dial has 99 positions. The puzzle input are the rotations.

    """

    def part_one(self, input: utils.Input) -> str | int:
        start = 50
        hit_zero = 0
        for match in input.lines().parse("{dir}{rotations:d}"):
            direction = match["dir"]
            rotations = match["rotations"]
            match direction:
                case "L":
                    start -= rotations
                case "R":
                    start += rotations
            start %= 100
            if start == 0:
                hit_zero += 1
        return hit_zero

    def part_two(self, input: utils.Input) -> str | int:
        start = 50
        hit_zero = 0
        for match in input.lines().parse("{dir}{rotations:d}"):
            direction = match["dir"]
            rotations = match["rotations"]
            match direction:
                case "L":
                    for _ in range(rotations):
                        start -= 1
                        start %= 100
                        if start == 0:
                            hit_zero += 1
                case "R":
                    for _ in range(rotations):
                        start += 1
                        start %= 100
                        if start == 0:
                            hit_zero += 1
        return hit_zero


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=1,
        test_answers=("3", "6"),
        test_input="""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""",
    )
    runner.cli()
