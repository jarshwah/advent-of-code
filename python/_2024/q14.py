from collections import Counter
from dataclasses import dataclass
from math import prod

import utils

type Point = utils.Point
type Robots = list[Robot]
type Bounds = tuple[int, int]
type QuadrantScore = tuple[int, int, int, int]


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def move(self, steps: int, bounds: Bounds) -> None:
        self.x = (self.x + self.vx * steps) % bounds[0]
        self.y = (self.y + self.vy * steps) % bounds[1]


class Puzzle(utils.Puzzle):
    def get_bounds(self, input: utils.Input) -> Bounds:
        return (11, 7) if input.data == self.test_input else (101, 103)

    def part_one(self, input: utils.Input) -> str | int:
        """
        Move the robots 100 times, then calculate the score for each quadrant.

        The answer is the product of the scores.
        """
        bounds = self.get_bounds(input)
        robots: Robots = []
        for x, y, vx, vy in input.lines().scan_ints():
            robots.append(Robot(x, y, vx, vy))

        for robot in robots:
            robot.move(100, bounds)

        scores = quadrant_scores(robots, bounds)
        return prod(scores)

    def part_two(self, input: utils.Input) -> str | int:
        """
        Find the number of iterations for the robots to draw a xmas tree.

        The answer is the number of iterations.
        """
        bounds = self.get_bounds(input)
        robots: Robots = []
        for x, y, vx, vy in input.lines().scan_ints():
            robots.append(Robot(x, y, vx, vy))

        clones = [Robot(robot.x, robot.y, robot.vx, robot.vy) for robot in robots]

        scores: dict[int, QuadrantScore] = {}
        for s in range(1, bounds[0] * bounds[1] + 1):
            for robot in robots:
                robot.move(1, bounds)
            # Assume the drawing is approximately in the middle, excluding many
            # of the robots from the quadrant score.
            score = quadrant_scores(robots, bounds)
            scores[s] = score

        min_score = min(scores, key=lambda s: prod(scores[s]))
        for clone in clones:
            clone.move(min_score, bounds)
        draw(min_score, bounds, clones)
        return min_score


def draw(seconds: int, bounds: Bounds, robots: Robots) -> None:
    counter: Counter[Point] = Counter()
    for robot in robots:
        counter[(robot.x, robot.y)] += 1

    print(f"After {seconds} seconds:")
    for Y in range(bounds[1]):
        for X in range(bounds[0]):
            if (X, Y) in counter:
                print(counter[(X, Y)], end="")
            else:
                print(".", end="")
        print()
    print()


def quadrant_scores(robots: Robots, bounds: Bounds) -> QuadrantScore:
    """
    Return the score for each quadrant.
    """
    mid_x, mid_y = bounds[0] // 2, bounds[1] // 2
    scores = [0, 0, 0, 0]

    for robot in robots:
        if robot.x < mid_x:
            if robot.y < mid_y:
                scores[0] += 1
            elif robot.y > mid_y:
                scores[1] += 1
        elif robot.x > mid_x:
            if robot.y < mid_y:
                scores[2] += 1
            elif robot.y > mid_y:
                scores[3] += 1
    return tuple(scores)  # type: ignore


puzzle = Puzzle(
    year=2024,
    day=14,
    test_answers=("12", "5"),
    test_input="""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""",
)

if __name__ == "__main__":
    puzzle.cli()
