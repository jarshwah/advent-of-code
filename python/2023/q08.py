import itertools
import math

import aocd
from parse import parse

import utils


def part_one(raw: str) -> int:
    [[directions], network] = utils.Input(raw).group(sep="\n").strings

    indexes = itertools.cycle([int(lr) for lr in directions.replace("L", "0").replace("R", "1")])
    nodes = {
        parsed["start"]: (parsed["left"], parsed["right"])
        for line in network
        if (parsed := parse("{start} = ({left}, {right})", line))
    }
    node = "AAA"
    for move_number, index in enumerate(indexes, 1):
        node = nodes[node][index]
        if node == "ZZZ":
            return move_number


def part_two(raw: str) -> int:
    [[directions], network] = utils.Input(raw).group(sep="\n").strings
    dirs = len(directions)
    nodes = {
        parsed["start"]: (parsed["left"], parsed["right"])
        for line in network
        if (parsed := parse("{start} = ({left}, {right})", line))
    }
    starting_nodes = [key for key in nodes.keys() if key.endswith("A")]
    steps_to_end: list[int] = []
    for node in starting_nodes:
        step = 0
        while True:
            current_position = step % dirs
            node = nodes[node][directions[current_position] == "R"]
            if node.endswith("Z"):
                steps_to_end.append(step + 1)
                break
            step += 1
    return math.lcm(*steps_to_end)


def test():
    answer_1 = part_one(
        """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    )
    answer_2 = part_two(
        """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    )
    assert answer_1 == 6, answer_1
    assert answer_2 == 6, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=8, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
