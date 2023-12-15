from __future__ import annotations

from functools import reduce

import aocd

import utils


def hashed(s: str, start: int = 0) -> int:
    return reduce(lambda total, ch: ((ord(ch) + total) * 17) % 256, s, start)


def part_one(raw: str) -> int:
    sequences = utils.Input(raw).string.strip("\n").split(",")
    return sum(hashed(seq) for seq in sequences)


def part_two(raw: str) -> int:
    sequences = utils.Input(raw).string.strip("\n").replace("-", "").split(",")
    boxes: list[dict[str, int]] = [{} for _ in range(256)]
    for seq in sequences:
        match seq.split("="):
            case [label, focal]:
                box = boxes[hashed(label)]
                box.setdefault(label, int(focal))
                box[label] = int(focal)
            case [label]:
                boxes[hashed(label)].pop(label, None)
    power = 0
    for bn, box in enumerate(boxes, 1):
        for sn, lens in enumerate(box, 1):
            power += bn * sn * box[lens]
    return power


def test():
    test_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 1320, answer_1
    assert answer_2 == 145, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=15, year=2023)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
