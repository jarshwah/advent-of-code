from __future__ import annotations

import dataclasses
from collections import deque
from functools import reduce

import aocd

import utils


@dataclasses.dataclass()
class Lens:
    label: str
    focal: int

    def __eq__(self, other: Lens) -> bool:
        return self.label == other.label


def hashed(s: str, start: int = 0) -> int:
    return reduce(lambda total, ch: ((ord(ch) + total) * 17) % 256, s, start)


def part_one(raw: str) -> int:
    sequences = utils.Input(raw).string.strip("\n").split(",")
    return sum(hashed(seq) for seq in sequences)


def part_two(raw: str) -> int:
    boxes: list[deque] = []
    for _ in range(256):
        boxes.append(deque())

    sequences = utils.Input(raw).string.strip("\n").split(",")
    for seq in sequences:
        if "=" in seq:
            label, focal = seq.split("=")
            lens = Lens(label, int(focal))
            box = boxes[hashed(label)]
            try:
                idx = box.index(lens)
                box[idx].focal = lens.focal
            except ValueError:
                box.append(lens)
        else:
            label = seq.split("-")[0]
            try:
                boxes[hashed(label)].remove(Lens(label, 0))
            except ValueError:
                pass
    power = 0
    for bn, box in enumerate(boxes, 1):
        for sn, lens in enumerate(box, 1):
            power += bn * sn * lens.focal
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
