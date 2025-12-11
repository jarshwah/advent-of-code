from functools import cache

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        graph: dict[str, set[str]] = {}
        for line in input.lines().strings:
            head = line[:3]
            tail = set(line[5:].split(" "))
            graph[head] = tail

        def recurse(node: str) -> int:
            return 1 if node == "out" else sum(recurse(descendent) for descendent in graph[node])

        return recurse("you")

    def part_two(self, input: utils.Input) -> str | int:
        graph: dict[str, set[str]] = {}
        for line in input.lines().strings:
            head = line[:3]
            tail = set(line[5:].split(" "))
            graph[head] = tail

        @cache
        def recurse(node: str, dac: bool, fft: bool) -> int:
            if node == "out":
                return 1 if dac and fft else 0
            return sum(
                recurse(descendent, dac or node == "dac", fft or node == "fft")
                for descendent in graph[node]
            )

        return recurse("svr", False, False)


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=11,
        test_answers=("5", "2"),
        test_input="""aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""",
        test_input_2="""svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""",
    )
    runner.cli()
