from functools import cache

import utils


class Puzzle(utils.Puzzle):
    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        [all_available], designs = input.group(sep="\n").strings
        available = all_available.split(", ")

        @cache
        def check_pattern(design: str) -> int:
            if not design:
                return 1
            return sum(
                check_pattern(design[len(pattern) :])
                for pattern in available
                if design.startswith(pattern)
            )

        matches = 0
        match_count = 0
        for design in designs:
            if cnt := check_pattern(design):
                matches += 1
                match_count += cnt
        return matches, match_count


if __name__ == "__main__":
    runner = Puzzle(
        year=2024,
        day=19,
        both=True,
        test_answers=("6", "16"),
        test_input="""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""",
    )
    runner.cli()
