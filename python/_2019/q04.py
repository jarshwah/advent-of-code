import utils


class Puzzle(utils.Puzzle):
    """--- Day 4: Secure Container ---"""

    def part_one(self, input: utils.Input) -> str | int:
        if self.testing:
            return "no-answer"

        def valid(n: int) -> bool:
            doubles = False
            ns = str(n)
            for n1, n2 in zip(ns, ns[1:]):
                if n1 == n2:
                    doubles = True
                if n2 < n1:
                    return False
            return doubles

        start, end = list(input.split("-").numbers)
        return sum(valid(check) for check in range(start, end + 1))

    def part_two(self, input: utils.Input) -> str | int:
        if self.testing:
            return "no-answer"

        def valid(n: int) -> bool:
            doubles = False
            ns = str(n)
            for idx in range(len(ns) - 1):
                if ns[idx] > ns[idx + 1]:
                    return False
                # consecutive doubles must not be triples or better
                if (
                    not doubles
                    and ns[idx] == ns[idx + 1]
                    and (idx + 2 >= len(ns) or ns[idx] != ns[idx + 2])
                    and (idx - 1 < 0 or ns[idx] != ns[idx - 1])
                ):
                    doubles = True
            return doubles

        start, end = list(input.split("-").numbers)
        return sum(valid(check) for check in range(start, end + 1))


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=4,
        test_answers=("no-answer", "no-answer"),
        test_input="""""",
    )
    runner.cli()
