import math
from collections import defaultdict, deque

import aocd

import utils
from utils import DOWN, LEFT, RIGHT, UP, Point

WALL = {"#"}
EMPTY = {"."}
DIRECTIONS = [UP, LEFT, (0, 0), DOWN, RIGHT]


def print_board(board: dict[Point, set[str]]):
    height, width = max(board)
    print()
    for rn in range(height + 1):
        row = []
        for cn in range(width + 1):
            tiles = list(board[rn, cn])
            if len(tiles) > 1:
                row.append(str(len(tiles)))
            else:
                row.append(tiles[0])
        print("".join(row))
    print()


def get_next_board(board: dict[Point, set[str]]) -> dict[Point, set[str]]:
    height, width = max(board)
    nb: dict[Point, set[str]] = defaultdict(set)
    for position, tiles in board.items():
        for tile in tiles:
            match tile:
                case "#":
                    nb[position].add("#")
                case ">":
                    next_pos = position[0], position[1] + 1
                    if board[next_pos] == WALL:
                        next_pos = position[0], 1
                    nb[next_pos].add(">")
                case "<":
                    next_pos = position[0], position[1] - 1
                    if board[next_pos] == WALL:
                        next_pos = position[0], width - 1
                    nb[next_pos].add("<")
                case "^":
                    next_pos = position[0] - 1, position[1]
                    if board[next_pos] == WALL:
                        next_pos = height - 1, position[1]
                    nb[next_pos].add("^")
                case "v":
                    next_pos = position[0] + 1, position[1]
                    if board[next_pos] == WALL:
                        next_pos = 1, position[1]
                    nb[next_pos].add("v")
                case _:
                    pass

    # Fill out the empty spaces
    for rownum in range(height + 1):
        for colnum in range(width + 1):
            loc = rownum, colnum
            if loc not in nb:
                nb[loc] = EMPTY
    return nb


def solve(raw: str) -> tuple[int, int]:
    start: dict[Point, set[str]] = {}
    rows = utils.Input(raw).lines().strings
    for rownum, row in enumerate(rows):
        for colnum, col in enumerate(row):
            start[rownum, colnum] = {col}
    boards = [start]
    # There are walls, don't count the walls
    height, width = max(start)
    # We already have the first state, so generate 1 less
    required = math.lcm(height - 1, width - 1) - 1

    # The boards will repeat based on the LCM of the width/height, so pre-generate them
    next_board = start
    for _ in range(required):
        next_board = get_next_board(next_board)
        boards.append(next_board)

    start = (0, 1)
    dest = (height, width - 1)

    trip_1 = traverse(boards, 0, start, dest)
    trip_2 = traverse(boards, trip_1, dest, start)
    trip_3 = traverse(boards, trip_2, start, dest)
    return trip_1, trip_3


def traverse(boards: list[dict[Point, set[str]]], step: int, start: Point, dest: Point) -> int:
    print(f"{step=} {start=} {dest=}")
    num_boards = len(boards)
    check_in_order = DIRECTIONS if start < dest else list(reversed(DIRECTIONS))
    seen = {}
    best = 1e9
    queue = deque([(start, step)])
    while queue:
        curr, step = queue.pop()
        step += 1
        board_num = step % num_boards

        if step >= best:
            continue

        # Have we been in this state at a lower step?
        key = (curr, board_num)
        at_step = seen.get(key, 1e9)
        if step >= at_step:
            continue
        seen[key] = step

        next_board = boards[board_num]
        possibles = utils.neighbours(curr, check_in_order)
        if dest in possibles:
            best = min(best, step)
            continue
        queue.extend(
            ((pos, step) for pos in possibles if pos in next_board and next_board[pos] == EMPTY)
        )

    return best


def test():
    test_input = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""
    answer_1, answer_2 = solve(test_input)
    assert answer_1 == 18, answer_1
    assert answer_2 == 54, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=24, year=2022)
    a1, a2 = solve(data)
    print("Part 1: ", a1)
    print("Part 2: ", a2)
