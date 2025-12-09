import itertools

import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        points = [(pair[0], pair[1]) for pair in input.lines().split(",").integers]
        areas = sorted(
            [utils.Rect.from_corners(p1, p2).area for p1, p2 in itertools.combinations(points, 2)],
            reverse=True,
        )
        return areas[0]

    def part_two(self, input: utils.Input) -> str | int:
        points = [(pair[0], pair[1]) for pair in input.lines().split(",").integers]
        rectangles = sorted(
            [utils.Rect.from_corners(p1, p2) for p1, p2 in itertools.combinations(points, 2)],
            key=lambda box: box.area,
            reverse=True,
        )

        # complete the wrapping joining last -> first
        points.append(points[0])
        # Since all points are connected in order, it forms a perimeter of width-1 rects
        perimeter = {utils.Rect.from_corners(l1, l2) for l1, l2 in itertools.pairwise(points)}

        # So find the biggest rectangle that does not breach the perimeter
        for rect in rectangles:
            if not any(rect.overlaps(line_box) for line_box in perimeter):
                return rect.area
        return 0


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
