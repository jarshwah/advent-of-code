from more_itertools import windowed
import utils


def find_marker(raw: str, marker: int) -> int:
    for idx, substr in enumerate(windowed(raw, marker)):
        if len(set(substr)) == marker:
            return idx + marker
    return 1


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        return find_marker(raw, 4)

    def part_two(self, input: utils.Input) -> str | int:
        return find_marker(raw, 14)


puzzle = Puzzle(
    year=2022,
    day=6,
    test_answers=("11", "29"),
    test_input="""zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw""",
    test_input_2="""nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg""",
)

if __name__ == "__main__":
    puzzle.cli()
