import itertools
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        numbers = ["".join(reversed(num)) for num in input.string.splitlines()]
        max_cols = max(len(n) for n in numbers)
        answer = [0] * max_cols
        # Add up all of the numbers and carry over what we need
        zipped = itertools.zip_longest(*numbers, fillvalue="0")
        for pos, columns in enumerate(zipped):
            total = sum(TONUM[c] for c in columns) + answer[pos]
            if not (-2 <= total <= 2):
                mults, _ = divmod(total + 2, 5)
                answer[pos + 1] += mults
                total -= 5 * mults
            answer[pos] = total
        return "".join(TOCHAR[a] for a in reversed(answer))


puzzle = Puzzle(
    year=2022,
    day=25,
    test_answers=("", ""),
    test_input="""\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122""",
)

if __name__ == "__main__":
    puzzle.cli()
