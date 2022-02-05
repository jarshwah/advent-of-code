import aocd

import utils

flipper = str.maketrans("01", "10")


def parse(data: str) -> tuple[str, utils.Grid[str]]:
    algo, grid_str = data.split("\n\n")
    grid = utils.Grid(rows=grid_str.splitlines())
    return algo, grid


def enhance(algo: str, pixels: set[utils.Point], iterations: int, printer: bool = False) -> int:
    print_pixels(pixels, printer)
    flasher = algo[0] == "#"
    for n in range(iterations):
        save_pixel = "." if flasher and (n % 2 == 0) else "#"
        new_pixels: set[utils.Point] = set()
        # Our minimum value can be the bottom right pixel, so we need to extend
        # out in all directions.
        rlo, rhi, clo, chi = get_bounds(pixels)
        for ri in range(rlo - 3, rhi + 3):
            for ci in range(clo - 3, chi + 3):
                point = (ri, ci)
                neighbours = utils.neighbours(point, utils.DIRECTIONS_9)
                pixel_key = "".join(["1" if nb in pixels else "0" for nb in neighbours])
                if flasher and save_pixel == "#":
                    # Current pixels are OFF, so flip the key bits
                    pixel_key = pixel_key.translate(flipper)
                new_value = algo[int(pixel_key, 2)]
                if new_value == save_pixel:
                    new_pixels.add(point)
        pixels = new_pixels
        print_pixels(pixels, printer)
    return len(pixels)


def print_pixels(pixels: set[utils.Point], print_it: bool) -> None:
    if not print_it:
        return
    rlo, rhi, clo, chi = get_bounds(pixels)
    for ri in range(rlo, rhi + 1):
        row = []
        for ci in range(clo, chi + 1):
            p = (ri, ci)
            row.append("#" if p in pixels else ".")
        print("".join(row))
    print()


def get_bounds(pixels: set[utils.Point]) -> tuple[int, int, int, int]:
    rlo = int(min(r for r, c in pixels))
    rhi = int(max(r for r, c in pixels))
    clo = int(min(c for r, c in pixels))
    chi = int(max(c for r, c in pixels))
    return rlo, rhi, clo, chi


def part_one(data: str) -> int:
    algo, grid = parse(data)
    pixels = {p for p in grid if grid[p] == "#"}
    return enhance(algo, pixels, 2)


def part_two(data: str) -> int:
    algo, grid = parse(data)
    pixels = {p for p in grid if grid[p] == "#"}
    return enhance(algo, pixels, 50)


def test():
    test_input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 35, answer_1
    assert answer_2 == 3351, answer_2


if __name__ == "__main__":
    # test()
    data = aocd.get_data(day=20, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
