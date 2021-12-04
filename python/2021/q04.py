import itertools
from collections import defaultdict
from typing import Dict, Set, Tuple

import aocd

Lookup = Dict[int, Set[Tuple[int, int, int]]]
Row = list[int]
Board = list[Row]
Boards = list[Board]
Numbers = list[int]


def parse_input(data: str) -> Tuple[list[Board], Numbers, Lookup]:
    lines = data.splitlines()
    numbers: Numbers = [int(num) for num in lines[0].split(",")]
    board: Board = []
    boards: Boards = [board]
    # Stash a lookup of number -> [(board, row, col), ...] triples
    lookup: Lookup = defaultdict(set)
    for line in lines[2:]:
        if line.strip() == "":
            # empty-line == new board
            board = []
            boards.append(board)
            continue
        board_num = len(boards) - 1
        row_pos = len(board)
        row = []
        for col_pos, num in enumerate(line.split()):
            row.append(int(num))
            lookup[int(num)].add((board_num, row_pos, col_pos))
        board.append(row)
    return boards, numbers, lookup


def check_bingo(boards: Boards, board_num: int, row_pos: int, col_pos: int) -> bool:
    if sum(boards[board_num][row_pos]) == -5:
        return True
    if sum(row[col_pos] for row in boards[board_num]) == -5:
        return True
    return False


def part_one(data: str) -> int:
    boards, numbers, lookup = parse_input(data)
    for number in numbers:
        for board_num, row_pos, col_pos in lookup[number]:
            boards[board_num][row_pos][col_pos] = -1
            if check_bingo(boards, board_num, row_pos, col_pos):
                return sum(num for num in itertools.chain(*boards[board_num]) if num > 0) * number
    return -1


def part_two(data: str) -> int:
    boards, numbers, lookup = parse_input(data)
    finished = set()
    for number in numbers:
        for board_num, row_pos, col_pos in lookup[number]:
            if board_num in finished:
                continue
            boards[board_num][row_pos][col_pos] = -1
            if check_bingo(boards, board_num, row_pos, col_pos):
                finished.add(board_num)
                if len(finished) == len(boards):
                    return (
                        sum(num for num in itertools.chain(*boards[board_num]) if num > 0) * number
                    )


def test():
    test_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
    answer_1 = part_one(test_input)
    answer_2 = part_two(test_input)
    assert answer_1 == 4512, answer_1
    assert answer_2 == 1924, answer_2


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=4, year=2021)
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
