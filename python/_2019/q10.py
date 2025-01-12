import math

import utils

type Point = utils.Point


class Puzzle(utils.Puzzle):
    """--- Day 10: Monitoring Station ---"""

    def both_parts(self, input: utils.Input) -> tuple[str | int, str | int]:
        grid = input.grid()
        asteroids: dict[Point, dict[float, Point]] = {ast: {} for ast in grid.find_all("#")}
        for asteroid in asteroids:
            for other in asteroids:
                if other == asteroid:
                    continue
                angle = math.atan2(other[0] - asteroid[0], other[1] - asteroid[1])
                if angle not in asteroids[asteroid]:
                    asteroids[asteroid][angle] = other

        best_view = 0
        best_angles = None
        for angs in asteroids.values():
            if len(angs) >= best_view:
                best_view = len(angs)
                best_angles = angs

        if self.testing or not best_angles:
            return best_view, "no-answer"

        angles = sorted(best_angles)
        # rotate, so that UP is first (UP is in the list... right?)
        UP = math.atan2(-1, 0)
        idx = angles.index(UP)
        angles = angles[idx:] + angles[:idx]
        a_200th = best_angles[angles[200 - 1]]

        return best_view, a_200th[1] * 100 + a_200th[0]


if __name__ == "__main__":
    runner = Puzzle(
        year=2019,
        day=10,
        both=True,
        test_answers=("8", "no-answer"),
        test_input=""".#..#
.....
#####
....#
...##""",
    )
    runner.cli()
