import itertools

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        points = [(pair[0], pair[1]) for pair in input.lines().split(",").integers]
        areas = sorted(
            [manhattan_area(p1, p2) for p1, p2 in itertools.combinations(points, 2)], reverse=True
        )
        return areas[0]

    def part_two(self, input: utils.Input) -> str | int:
        points = [(pair[0], pair[1]) for pair in input.lines().split(",").integers]
        areas = sorted(
            [
                (manhattan_area(p1, p2), boxify(p1, p2))
                for p1, p2 in itertools.combinations(points, 2)
            ],
            reverse=True,
        )
        wrapped = points + [points[0]]
        green_lines: set[utils.Point4d] = set()
        for l1, l2 in zip(wrapped, wrapped[1:]):
            green_lines.add(boxify(l1, l2))

        for area, box in areas:
            if not any(box_overlaps(box, line_box) for line_box in green_lines):
                return area
        return 0


def manhattan_area(p1: utils.Point, p2: utils.Point) -> int:
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def boxify(p1: utils.Point, p2: utils.Point) -> utils.Point4d:
    return (min(p1[0], p2[0]), max(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[1], p2[1]))


def line_overlaps(l1: utils.Point, l2: utils.Point) -> bool:
    # We allow the line to *touch* > but not *cross* >=
    return max(l1) > min(l2) and max(l2) > min(l1)


def box_overlaps(b1: utils.Point4d, b2: utils.Point4d) -> bool:
    # fmt: off
    return (
        line_overlaps((b1[0], b1[1]), (b2[0], b2[1])) and
        line_overlaps((b1[2], b1[3]), (b2[2], b2[3])
        )
    )
    # fmt: on


if __name__ == "__main__":
    runner = Puzzle(
        year=2025,
        day=9,
        test_answers=("50", "24"),
        test_input="""7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""",
    )
    runner.cli()
