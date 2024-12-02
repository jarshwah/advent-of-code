import datetime
import pathlib

TEMPLATE = """
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str:
        return ""

    def part_two(self, input: utils.Input) -> str:
        return ""


if __name__ == "__main__":
    runner = Puzzle(
        year={year},
        day={day},
        test_answers=("", ""),
        test_input=\"\"\"\"\"\",
    )
    runner.cli()
"""


def create(day: int, year: int) -> None:
    here = pathlib.Path(__file__).parent
    year_dir = here / f"_{year}"
    if not year_dir.exists():
        raise ValueError(f"We do not yet have a {year} for puzzles.")
    puzzle_file = year_dir / f"q{day:02d}.py"

    if puzzle_file.exists():
        raise ValueError(f"We already have a puzzle {year}/{puzzle_file.name}")

    print(f"Creating {puzzle_file}")
    with puzzle_file.open("w") as f:
        f.write(TEMPLATE.format(year=year, day=day))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("--year", type=int, default=datetime.datetime.now().year)
    args = parser.parse_args()
    create(args.day, args.year)
