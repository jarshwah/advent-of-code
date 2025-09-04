import utils


class Puzzle(utils.Puzzle):
    def part_one(self, input: utils.Input) -> str | int:
        current = (0, 0)
        points = [current]
        lines = input.lines().strings
        for line in lines:
            direction, steps_s, color = line.split()
            for _ in range(int(steps_s)):
                current = utils.point_add(current, DIRS[direction])
                points.append(current)
        return utils.area_including_boundary(points)

    def part_two(self, input: utils.Input) -> str | int:
        lines = input.lines().strings
        first = (0, 0)
        current = first
        num_points = 0
        area_gen = utils.shoelace_iter(first)
        next(area_gen)
        for line in lines:
            _, _, color = line.split()
            steps = int(color[2:7], 16)
            direction = color[7]
            num_points += steps
            current = utils.point_add(current, DIRS[direction], steps)
            area_gen.send(current)
        area = next(area_gen)
        return utils.picks_theorem(num_points, area)


puzzle = Puzzle(
    year=2023,
    day=18,
    test_answers=("62", "952408144115"),
    test_input="""\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""",
)

if __name__ == "__main__":
    puzzle.cli()
