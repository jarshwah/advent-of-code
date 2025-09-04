from __future__ import annotations
from functools import reduce
import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        sequences = utils.Input.string.strip("\n").split(",")
        return sum(hashed(seq) for seq in sequences)

    def part_two(self, input: utils.Input) -> str | int:
        sequences = utils.Input.string.strip("\n").replace("-", "").split(",")
        boxes: list[dict[str, int]] = [{} for _ in range(256)]
        for seq in sequences:
            match seq.split("="):
                case [label, focal]:
                    boxes[hashed(label)][label] = int(focal)
                case [label]:
                    boxes[hashed(label)].pop(label, None)

        return sum(
            bn * sn * box[lens] for bn, box in enumerate(boxes, 1) for sn, lens in enumerate(box, 1)
        )


puzzle = Puzzle(
    year=2023,
    day=15,
    test_answers=("1320", "145"),
    test_input="""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""",
)

if __name__ == "__main__":
    puzzle.cli()
