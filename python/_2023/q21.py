from collections import deque

import aocd

import utils


def part_one(raw: str, steps: int) -> int:
    for rn, row in enumerate(raw.splitlines()):
        for cn, char in enumerate(row):
            if char == "S":
                start = (rn, cn)
                break
    return solve(raw, steps, start)


def solve(raw: str, steps: int, start: utils.Point) -> int:
    grid = utils.Input(raw).grid()
    seen = {}
    parity = steps % 2
    assert grid[start] == "S"
    queue = deque([(start, 0)])
    while queue:
        # only steps matching parity are admissable
        point, steps_taken = queue.popleft()
        if point in seen:
            continue
        seen[point] = steps_taken

        if steps_taken >= steps:
            continue

        for neighbor in grid.get_neighbours(point):
            if grid[neighbor] == "#":
                continue
            queue.append((neighbor, steps_taken + 1))
    return len([p for p in seen if (seen[p] % 2) == parity])


def part_two(raw: str, steps: int) -> int:
    # expand the grid so it's big enough to do the 3 runs
    rows = []
    size = 0
    for _ in range(5):
        for row in raw.splitlines():
            size = len(row)
            rows.append(row * 5)
    big_raw = "\n".join(rows)

    # Assume we begin right in the center of the grid. Solve confirms a match.
    STEPS_A = size // 2
    STEPS_B = size + STEPS_A
    STEPS_C = size + STEPS_B
    # print(f"{STEPS_A=} {STEPS_B=} {STEPS_C=}")
    # Start is in the center of the 3x3 grid
    big_start = (STEPS_C, STEPS_C)
    # print(f"{big_start=}")
    # Solve the first grid, then the second grid (larger, different parity), then the third (same parity as first)
    s1 = solve(big_raw, STEPS_A, big_start)
    s2 = solve(big_raw, STEPS_B, big_start)
    s3 = solve(big_raw, STEPS_C, big_start)
    # print(f"{s1=} {s2=} {s3=}")

    # Then we can compute the quadratic sequence (like we did for day 9, but math'd)
    # https://www.radfordmathematics.com/algebra/sequences-series/difference-method-sequences/quadratic-sequences.html
    N = (steps - STEPS_A) // size
    D1 = s2 - s1
    D2 = s3 - s2
    D3 = D2 - D1
    return s1 + N * D1 + N * (N - 1) // 2 * D3


def test():
    test_input = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    answer_1 = part_one(test_input, 6)
    assert answer_1 == 16, answer_1


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=21, year=2023)
    print("Part 1: ", part_one(data, 64))
    print("Part 2: ", part_two(data, 26501365))
