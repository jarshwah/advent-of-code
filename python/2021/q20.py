from copy import deepcopy

import aocd

from utils import Grid

translator = str.maketrans(" .#", "001")


def parse(data: str) -> tuple[str, Grid[str]]:
    algo, grid_str = data.split("\n\n")
    grid = Grid(rows=grid_str.splitlines(), pad_with=".")
    return algo, grid


def part_one(data: str) -> int:
    algo, grid = parse(data)
    for _ in range(2):
        print(f"{min(grid)=} {max(grid)=}")
        grid.add_padding(".")
        grid.print()
        new_grid = Grid(rows=[], pad_with=".")
        points = sorted(grid.points.keys(), key=lambda t: (t[1], t[0]))
        for p in points:
            neighbours = sorted(
                list(grid.get_neighbours(p, diag=True)) + [p], key=lambda t: (t[1], t[0])
            )
            values = [str(grid[p]) for p in neighbours]
            bstr = "".join(values).translate(translator)
            new_value = algo[int(bstr, 2)]
            new_grid[p] = new_value
        grid = new_grid
    grid.print()
    return len([val for val in grid.points.values() if val == "#"])


def part_two(data: str) -> int:
    algo, grid = parse(data)
    return 1


def test():
    test_input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..## #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.### .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#. .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#..... .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.. ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#..... ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 35, answer_1
    assert answer_2 == 1, answer_2


if __name__ == "__main__":
    test()
    # data = aocd.get_data(day=20, year=2021)
    # print("Part 1: ", part_one(data))
    # print("Part 2: ", part_two(data))
