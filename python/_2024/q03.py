import re

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        """
        Sum together mul(x,y) instructions where x and y are 1-3 digit numbers.
        """
        return sum(
            int(x) * int(y) for x, y in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input.string)
        )

    def part_two(self, input: utils.Input) -> str | int:
        """
        Same as part one, but skip any mul instructions inside a don't() block, and resume after a do() block.
        """
        doing = True
        re_dont_mul = re.compile(r"don't\(\)|mul\((\d{1,3}),(\d{1,3})\)")
        re_do = re.compile(r"do\(\)")
        computation = 0
        search_string = input.string
        while search_string:
            if doing:
                if match := re_dont_mul.search(search_string):
                    x, y = match.groups()
                    if (x, y) != (None, None):
                        computation += int(x) * int(y)
                    else:
                        doing = False
                    search_string = search_string[match.end() :]
                    continue
            else:
                if match := re_do.search(search_string):
                    doing = True
                    search_string = search_string[match.end() :]
                    continue
            break  # no more matches
        return computation

    def part_two_alt(self, input: utils.Input) -> str | int:
        """
        Same as part one, but skip any mul instructions inside a don't() block, and resume after a do() block.
        """
        instructions = re.compile(r"(do)\(\)|(don't)\(\)|mul\((\d{1,3}),(\d{1,3})\)")
        doing = True
        computation = 0
        for inst in instructions.findall(input.string):
            match inst:
                case "do", *_:
                    doing = True  # type: ignore [unreachable]
                case _, "don't", *_:
                    doing = False  # type: ignore [unreachable]
                case (*_, x, y) if doing:
                    computation += int(x) * int(y)  # type: ignore [unreachable]
        return computation


puzzle = Puzzle(
    year=2024,
    day=3,
    test_answers=("161", "48"),
    test_input="""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""",
    test_input_2="""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))""",
)

if __name__ == "__main__":
    puzzle.cli()
