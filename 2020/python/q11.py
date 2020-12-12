import copy
import dataclasses
import itertools
import time
import typing as t
import terminaltables
from functools import lru_cache

import aocd

Place = t.Optional[bool]
Board = t.List[t.List[Place]]
Coords = t.Tuple[int, int]
Neighbours = t.List[Coords]


@dataclasses.dataclass
class GameOfSeats:
    boards: t.Tuple[Board, Board]
    board_pointer = 1

    def __init__(self, initial_state: t.List[str]):
        board_one: Board = []
        board_two: Board = []
        for line in initial_state:
            row: t.List[Place] = []
            row.append(None)
            for place in line:
                row.append(self.convert(place))
            row.append(None)
            board_one.append(row)
        # wrap the board in empty places to avoid bounds checking
        board_one.insert(0, [None] * len(board_one[0]))
        board_one.append([None] * len(board_one[0]))
        board_two = copy.deepcopy(board_one)
        self.boards = (board_one, board_two)

    def play(self, tolerance=4, immediate=True) -> int:
        changed = True
        generations = 0
        while changed:
            generations += 1
            self.board_pointer = not self.board_pointer
            changed = False
            source = self.boards[self.board_pointer]
            target = self.boards[not self.board_pointer]
            for y, row in enumerate(source):
                for x, place in enumerate(row):
                    if place is None:
                        target[y][x] = place
                    else:
                        neighbours = self.count_neighbours(y, x, immediate, self.board_pointer)
                        if place is False and neighbours == 0:
                            target[y][x] = True
                            changed = True
                        elif place is True and neighbours >= tolerance:
                            target[y][x] = False
                            changed = True
                        else:
                            target[y][x] = place
            # self.render(self.board_pointer)
        board = self.boards[self.board_pointer]
        return sum(filter(None, itertools.chain(*board)))

    def count_neighbours(self, y: int, x: int, immediate: bool, board_pointer: int) -> int:
        board = self.boards[board_pointer]
        if board[y][x] is None:
            return 0

        neighbours = self.get_neighbours(y, x, immediate)
        return sum(bool(board[cy][cx]) for cy, cx in neighbours)

    def get_neighbours(self, y: int, x: int, immediate: bool) -> Neighbours:
        if immediate:
            return self._get_immediate_neighbours(y, x)
        return self._get_neighbours_los(y, x)

    def _get_immediate_neighbours(self, y, x):
        # fmt: off
        return (
            [
                (y - 1, x),      # top
                (y - 1, x - 1),  # top left
                (y, x - 1),      # left
                (y + 1, x - 1),  # bottom left
                (y + 1, x),      # bottom
                (y + 1, x + 1),  # bottom right
                (y, x + 1),      # right
                (y - 1, x + 1),  # top right
            ]
        )
        # fmt: on

    def _get_neighbours_los(self, y, x) -> Neighbours:
        # which board does not matter
        board = self.boards[self.board_pointer]
        place = board[y][x]
        if place is None:
            return []

        y_len = len(board) - 1
        x_len = len(board[0]) - 1

        @lru_cache(maxsize=None)
        def get(y: int, x: int):
            return list(
                filter(
                    None,
                    [
                        # top
                        self.get_neighbour(
                            (y, x), lambda cy, cx: cy > 0, lambda cy, cx: (cy - 1, cx)
                        ),
                        # top left
                        self.get_neighbour(
                            (y, x),
                            lambda cy, cx: cy > 0 and cx > 0,
                            lambda cy, cx: (cy - 1, cx - 1),
                        ),
                        # left
                        self.get_neighbour(
                            (y, x), lambda cy, cx: cx > 0, lambda cy, cx: (cy, cx - 1)
                        ),
                        # bottom left
                        self.get_neighbour(
                            (y, x),
                            lambda cy, cx: cy < y_len and cx > 0,
                            lambda cy, cx: (cy + 1, cx - 1),
                        ),
                        # bottom
                        self.get_neighbour(
                            (y, x), lambda cy, cx: cy < y_len, lambda cy, cx: (cy + 1, cx)
                        ),
                        # bottom right
                        self.get_neighbour(
                            (y, x),
                            lambda cy, cx: cy < y_len and cx < x_len,
                            lambda cy, cx: (cy + 1, cx + 1),
                        ),
                        # right
                        self.get_neighbour(
                            (y, x), lambda cy, cx: cx < x_len, lambda cy, cx: (cy, cx + 1)
                        ),
                        # top right
                        self.get_neighbour(
                            (y, x),
                            lambda cy, cx: cy > 0 and cx < x_len,
                            lambda cy, cx: (cy - 1, cx + 1),
                        ),
                    ],
                )
            )

        return get(y, x)

    def get_neighbour(
        self,
        position: Coords,
        iter_func: t.Callable[[int, int], bool],
        direction_func: t.Callable[[int, int], Coords],
    ) -> t.Optional[Coords]:
        board = self.boards[self.board_pointer]
        cy, cx = position
        while iter_func(cy, cx):
            cy, cx = direction_func(cy, cx)
            if board[cy][cx] is not None:
                return cy, cx
        return None

    @staticmethod
    def convert(place: str) -> Place:
        if place == "#":
            return True
        if place == "L":
            return False
        if place == ".":
            return None
        raise ValueError

    def render(self, board_pointer):
        orig_board = self.boards[board_pointer]
        board = copy.deepcopy(orig_board)
        for y, row in enumerate(orig_board):
            for x, place in enumerate(row):
                if place is None:
                    board[y][x] = "."
                elif place is True:
                    board[y][x] = "#"
                elif place is False:
                    board[y][x] = "L"
        table = terminaltables.AsciiTable(board)
        table.padding_left = 0
        table.padding_right = 0
        table.inner_column_border = False
        table.inner_footing_row_border = False
        table.inner_heading_row_border = False
        table.inner_row_border = False
        table.outer_border = False
        print(table.table)
        print()
        print()
        print()
        time.sleep(0.01)


def part_one(data: t.List[str]) -> int:
    game = GameOfSeats(data)
    return game.play(tolerance=4, immediate=True)


def part_two(data: t.List[str]) -> int:
    game = GameOfSeats(data)
    return game.play(tolerance=5, immediate=False)


if __name__ == "__main__":
    data = aocd.get_data(day=11, year=2020).splitlines()
    print("Part 1: ", part_one(data))
    print("Part 2: ", part_two(data))
